from __future__ import annotations

from typing import List, Union, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/giveaways", tags=["Giveaway Creation & Management"])

################################################################################
def full_giveaway_select(
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    embed_id: Optional[int] = None
):

    query = deps.db.query(Models.GiveawayModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.GiveawayModel.details),
        selectinload(Models.GiveawayModel.entries),
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert embed_id is not None
        return query.filter_by(id=embed_id).first()

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=Schemas.DeepGiveawayManagerSchema, summary="Get the Giveaway Manager of the provided the guild")
async def get_giveaway_manager(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepGiveawayManagerSchema:

    manager = deps.db.query(Models.GiveawayManagerModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.GiveawayManagerModel.giveaways).selectinload(Models.GiveawayModel.details),
        selectinload(Models.GiveawayManagerModel.giveaways).selectinload(Models.GiveawayModel.entries),
    ).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Giveaway Manager not found for this guild.")

    return Schemas.DeepGiveawayManagerSchema.model_validate(manager)

################################################################################
@router.get("/{giveaway_id}", response_model=Schemas.DeepGiveawaySchema, summary="Get a specific Giveaway by its ID")
async def get_giveaway(
    giveaway_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepGiveawaySchema:

    giveaway = get_shallow_or_404(deps.db, Models.GiveawayModel, id=giveaway_id)
    match_or_403(deps.guild_id, giveaway.guild_id)

    return Schemas.DeepGiveawaySchema.model_validate(giveaway)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.DeepGiveawaySchema, summary="Create a new Giveaway")
async def create_giveaway(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepGiveawaySchema:

    giveaway = Models.GiveawayModel(guild_id=deps.guild_id)
    deps.db.add(giveaway)
    deps.db.flush()
    deps.db.refresh(giveaway)

    details = Models.GiveawayDetailsModel(giveaway_id=giveaway.id)
    deps.db.add(details)
    deps.db.flush()

    giveaway = full_giveaway_select(deps, "Single", giveaway.id)
    audit_log_create(deps, giveaway, giveaway.id)

    return Schemas.DeepGiveawaySchema.model_validate(giveaway)

################################################################################
@router.post("/{giveaway_id}/entries", status_code=201, response_model=Schemas.GiveawayEntrySchema, summary="Add an entry to a Giveaway")
async def add_giveaway_entry(
    giveaway_id: int,
    data: Schemas.GiveawayEntryCreateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.GiveawayEntrySchema:

    giveaway = get_shallow_or_404(deps.db, Models.GiveawayModel, id=giveaway_id)
    match_or_403(deps.guild_id, giveaway.guild_id)

    entry = Models.GiveawayEntryModel(giveaway_id=giveaway.id, user_id=data.user_id)
    deps.db.add(entry)
    deps.db.flush()
    deps.db.refresh(entry)

    audit_log_create(deps, entry, entry.id)

    return Schemas.GiveawayEntrySchema.model_validate(entry)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{giveaway_id}", status_code=204, summary="Delete a Giveaway by its ID")
async def delete_giveaway(
    giveaway_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    giveaway = get_shallow_or_404(deps.db, Models.GiveawayModel, id=giveaway_id)
    match_or_403(deps.guild_id, giveaway.guild_id)

    deps.db.delete(giveaway)
    audit_log_delete(deps, giveaway, giveaway.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{giveaway_id}/entries/{entry_id}", status_code=204, summary="Delete an entry from a Giveaway")
async def delete_giveaway_entry(
    giveaway_id: int,
    entry_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    giveaway = get_shallow_or_404(deps.db, Models.GiveawayModel, id=giveaway_id)
    match_or_403(deps.guild_id, giveaway.guild_id)

    entry = get_shallow_or_404(deps.db, Models.GiveawayEntryModel, id=entry_id, giveaway_id=giveaway.id)
    match_or_403(giveaway.id, entry.giveaway_id)

    deps.db.delete(entry)
    audit_log_delete(deps, entry, entry.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/", response_model=Schemas.DeepGiveawayManagerSchema, summary="Update a Giveaway Manager by its Guild ID")
async def update_giveaway_manager(
    data: Schemas.GiveawayManagerUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepGiveawayManagerSchema:

    manager = get_shallow_or_404(deps.db, Models.GiveawayManagerModel, guild_id=deps.guild_id)

    apply_updates(manager, data)
    audit_log_update(deps, manager, manager.guild_id)

    deps.db.flush()
    deps.db.refresh(manager)

    return Schemas.DeepGiveawayManagerSchema.model_validate(manager)

################################################################################
@router.patch("/{giveaway_id}", response_model=Schemas.DeepGiveawaySchema, summary="Update a Giveaway by its ID")
async def update_giveaway(
    giveaway_id: int,
    data: Schemas.GiveawayUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepGiveawaySchema:

    giveaway = get_shallow_or_404(deps.db, Models.GiveawayModel, id=giveaway_id)
    match_or_403(deps.guild_id, giveaway.guild_id)

    apply_updates(giveaway, data)
    audit_log_update(deps, giveaway, giveaway.id)

    deps.db.flush()
    deps.db.refresh(giveaway)

    return Schemas.DeepGiveawaySchema.model_validate(giveaway)

################################################################################
@router.patch("/{giveaway_id}/details", response_model=Schemas.GiveawayDetailsSchema, summary="Update the details of a Giveaway")
async def update_giveaway_details(
    giveaway_id: int,
    data: Schemas.GiveawayDetailsUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.GiveawayDetailsSchema:

    giveaway = get_shallow_or_404(deps.db, Models.GiveawayModel, id=giveaway_id)
    match_or_403(deps.guild_id, giveaway.guild_id)

    details = get_shallow_or_404(deps.db, Models.GiveawayDetailsModel, giveaway_id=giveaway.id)

    apply_updates(details, data)
    audit_log_update(deps, details, details.giveaway_id)

    deps.db.flush()
    deps.db.refresh(giveaway.details)

    return Schemas.GiveawayDetailsSchema.model_validate(giveaway.details)

################################################################################
