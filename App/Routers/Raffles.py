from __future__ import annotations

from datetime import datetime
from typing import List, Union, Literal, Optional, Type

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/raffles", tags=["Raffle Management"])

################################################################################
def full_raffle_manager_select(deps: Dependencies) -> Type[Models.RaffleManagerModel]:

    manager = deps.db.query(Models.RaffleManagerModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.RaffleManagerModel.raffles).selectinload(Models.RaffleModel.entries),
    ).first()

    if not manager:
        raise HTTPException(status_code=404, detail="Raffle Manager not found for this guild.")

    return manager

################################################################################
def full_raffle_select(
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    raffle_id: Optional[int] = None
) -> Union[List[Type[Models.RaffleModel]], Type[Models.RaffleModel]]:

    query = deps.db.query(Models.RaffleModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.RaffleModel.entries),
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert raffle_id is not None
        return query.filter_by(id=raffle_id).first()

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=Schemas.DeepRaffleManagerSchema, summary="Get the Raffle Manager of the provided guild")
def get_raffle_manager(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepRaffleManagerSchema:

    manager = full_raffle_manager_select(deps)
    return Schemas.DeepRaffleManagerSchema.model_validate(manager)

################################################################################
@router.get("/{raffle_id}", response_model=Schemas.DeepRaffleSchema, summary="Get a specific Raffle by its ID")
def get_raffle(
    raffle_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepRaffleSchema:

    raffle = get_shallow_or_404(deps.db, Models.RaffleModel, id=raffle_id)
    match_or_403(deps.guild_id, raffle.guild_id)

    raffle = full_raffle_select(deps, mode="Single", raffle_id=raffle_id)
    return Schemas.DeepRaffleSchema.model_validate(raffle)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.DeepRaffleSchema, summary="Create a new Raffle")
def create_raffle(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepRaffleSchema:

    new_raffle = Models.RaffleModel(guild_id=deps.guild_id)
    deps.db.add(new_raffle)
    deps.db.flush()
    deps.db.refresh(new_raffle)

    audit_log_create(deps, new_raffle, new_raffle.id)
    return Schemas.DeepRaffleSchema.model_validate(new_raffle)

################################################################################
@router.post("/{raffle_id}/entries", status_code=201, response_model=Schemas.RaffleEntrySchema, summary="Create a new entry for a user in a Raffle")
def create_raffle_entry(
    raffle_id: int,
    data: Schemas.RaffleEntryCreateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.RaffleEntrySchema:

    raffle = get_shallow_or_404(deps.db, Models.RaffleModel, id=raffle_id)
    match_or_403(deps.guild_id, raffle.guild_id)

    entry = Models.RaffleEntryModel(raffle_id=raffle.id, **data.model_dump())
    deps.db.add(entry)
    deps.db.flush()
    deps.db.refresh(entry)

    audit_log_create(deps, entry, entry.id)
    return Schemas.RaffleEntrySchema.model_validate(entry)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{raffle_id}", status_code=204, summary="Delete a Raffle by its ID")
def delete_raffle(
    raffle_id: int,
    deps: Dependencies = Depends(get_dependencies)
):

    raffle = get_shallow_or_404(deps.db, Models.RaffleModel, id=raffle_id)

    deps.db.delete(raffle)
    audit_log_delete(deps, raffle, raffle.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{raffle_id}/entries/{entry_id}", status_code=204, summary="Delete a Raffle Entry by its ID")
def delete_raffle_entry(
    raffle_id: int,
    entry_id: int,
    deps: Dependencies = Depends(get_dependencies)
):

    raffle = get_shallow_or_404(deps.db, Models.RaffleModel, id=raffle_id)
    match_or_403(deps.guild_id, raffle.guild_id)

    entry = get_shallow_or_404(deps.db, Models.RaffleEntryModel, id=entry_id, raffle_id=raffle.id)
    match_or_403(raffle.id, entry.raffle_id)

    deps.db.delete(entry)
    audit_log_delete(deps, entry, entry.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/", response_model=Schemas.DeepRaffleManagerSchema, summary="Update the Raffle Manager")
def update_raffle_manager(
    data: Schemas.RaffleManagerUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepRaffleManagerSchema:

    manager = full_raffle_manager_select(deps)

    apply_updates(manager, data)
    audit_log_update(deps, manager, manager.guild_id)

    deps.db.flush()
    deps.db.refresh(manager)

    return Schemas.DeepRaffleManagerSchema.model_validate(manager)

################################################################################
@router.patch("/{raffle_id}", response_model=Schemas.DeepRaffleSchema, summary="Update a Raffle by its ID")
def update_raffle(
    raffle_id: int,
    data: Schemas.RaffleUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepRaffleSchema:

    raffle = get_shallow_or_404(deps.db, Models.RaffleModel, id=raffle_id)
    match_or_403(deps.guild_id, raffle.guild_id)

    apply_updates(raffle, data)
    audit_log_update(deps, raffle, raffle.id)

    deps.db.flush()
    deps.db.refresh(raffle)

    return Schemas.DeepRaffleSchema.model_validate(raffle)

################################################################################
@router.patch("/{raffle_id}/entries/{entry_id}", response_model=Schemas.RaffleEntrySchema, summary="Update a Raffle Entry by its ID")
def update_raffle_entry(
    raffle_id: int,
    entry_id: int,
    data: Schemas.RaffleEntryUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.RaffleEntrySchema:

    raffle = get_shallow_or_404(deps.db, Models.RaffleModel, id=raffle_id)
    match_or_403(deps.guild_id, raffle.guild_id)

    entry = get_shallow_or_404(deps.db, Models.RaffleEntryModel, id=entry_id, raffle_id=raffle.id)
    match_or_403(raffle.id, entry.raffle_id)

    apply_updates(entry, data)
    audit_log_update(deps, entry, entry.id)

    deps.db.flush()
    deps.db.refresh(entry)

    return Schemas.RaffleEntrySchema.model_validate(entry)

################################################################################
