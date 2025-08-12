from __future__ import annotations

from datetime import datetime
from typing import List, Union, Literal, Optional, Type

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/reaction-roles", tags=["Discord Reaction Role Management"])

################################################################################
def full_reaction_role_message_select(
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    reaction_role_id: Optional[int] = None
) -> Union[List[Type[Models.ReactionRoleMessageModel]], Type[Models.ReactionRoleMessageModel]]:

    query = deps.db.query(Models.ReactionRoleMessageModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.ReactionRoleMessageModel.roles)
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert reaction_role_id is not None
        return query.filter_by(id=reaction_role_id).first()

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=Schemas.DeepReactionRoleManagerSchema)
def get_reaction_role_manager(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepReactionRoleManagerSchema:

    manager = get_shallow_or_404(deps.db, Models.ReactionRoleManagerModel, guild_id=deps.guild_id)
    manager = deps.db.query(Models.ReactionRoleManagerModel).filter_by(guild_id=manager.guild_id).options(
        selectinload(Models.ReactionRoleManagerModel.messages).selectinload(Models.ReactionRoleMessageModel.roles)
    ).first()
    return Schemas.DeepReactionRoleManagerSchema.model_validate(manager)

################################################################################
@router.get("/{message_id}", response_model=Schemas.DeepReactionRoleMessageSchema)
def get_reaction_role_message(
    message_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepReactionRoleMessageSchema:

    message = get_shallow_or_404(deps.db, Models.ReactionRoleMessageModel, id=message_id)
    match_or_403(deps.guild_id, message.guild_id)

    message = full_reaction_role_message_select(deps, "Single", reaction_role_id=message.id)
    return Schemas.DeepReactionRoleMessageSchema.model_validate(message)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.DeepReactionRoleMessageSchema)
def create_reaction_role_message(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepReactionRoleMessageSchema:

    new_message = Models.ReactionRoleMessageModel(guild_id=deps.guild_id)

    deps.db.add(new_message)
    deps.db.flush()
    deps.db.refresh(new_message)

    audit_log_create(deps, new_message, new_message.id)
    return Schemas.DeepReactionRoleMessageSchema.model_validate(new_message)

################################################################################
@router.post("/{message_id}/roles", status_code=201, response_model=Schemas.ReactionRoleSchema)
def add_reaction_role(
    message_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ReactionRoleSchema:

    message = get_shallow_or_404(deps.db, Models.ReactionRoleMessageModel, id=message_id)
    match_or_403(deps.guild_id, message.guild_id)

    new_role = Models.ReactionRoleModel(message_id=message.id)

    deps.db.add(new_role)
    deps.db.flush()
    deps.db.refresh(new_role)

    audit_log_create(deps, new_role, new_role.id)
    return Schemas.ReactionRoleSchema.model_validate(new_role)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{message_id}", status_code=204)
def delete_reaction_role_message(
    message_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    message = get_shallow_or_404(deps.db, Models.ReactionRoleMessageModel, id=message_id)
    match_or_403(deps.guild_id, message.guild_id)

    deps.db.delete(message)
    audit_log_delete(deps, message, message.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{message_id}/roles/{role_id}", status_code=204)
def delete_reaction_role(
    message_id: int,
    role_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    message = get_shallow_or_404(deps.db, Models.ReactionRoleMessageModel, id=message_id)
    match_or_403(deps.guild_id, message.guild_id)

    role = get_shallow_or_404(deps.db, Models.ReactionRoleModel, id=role_id)
    match_or_403(message.id, role.message_id)

    deps.db.delete(role)
    audit_log_delete(deps, role, role.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/", response_model=Schemas.DeepReactionRoleManagerSchema)
def patch_reaction_role_manager(
    data: Schemas.ReactionRoleManagerUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepReactionRoleManagerSchema:

    manager = get_shallow_or_404(deps.db, Models.ReactionRoleManagerModel, guild_id=deps.guild_id)

    apply_updates(manager, data)
    audit_log_update(deps, manager, manager.guild_id)

    deps.db.flush()
    deps.db.refresh(manager)

    return Schemas.DeepReactionRoleManagerSchema.model_validate(manager)

################################################################################
@router.patch("/{message_id}", response_model=Schemas.DeepReactionRoleMessageSchema)
def patch_reaction_role_message(
    message_id: int,
    data: Schemas.ReactionRoleMessageUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepReactionRoleMessageSchema:

    message = get_shallow_or_404(deps.db, Models.ReactionRoleMessageModel, id=message_id)
    match_or_403(deps.guild_id, message.guild_id)

    apply_updates(message, data)
    audit_log_update(deps, message, message.id)

    deps.db.flush()
    deps.db.refresh(message)

    return Schemas.DeepReactionRoleMessageSchema.model_validate(message)

################################################################################
@router.patch("/{message_id}/roles/{role_id}", response_model=Schemas.ReactionRoleSchema)
def patch_reaction_role(
    message_id: int,
    role_id: int,
    data: Schemas.ReactionRoleUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ReactionRoleSchema:

    message = get_shallow_or_404(deps.db, Models.ReactionRoleMessageModel, id=message_id)
    match_or_403(deps.guild_id, message.guild_id)

    role = get_shallow_or_404(deps.db, Models.ReactionRoleModel, id=role_id)
    match_or_403(message.id, role.message_id)

    apply_updates(role, data)
    audit_log_update(deps, role, role.id)

    deps.db.flush()
    deps.db.refresh(role)

    return Schemas.ReactionRoleSchema.model_validate(role)

################################################################################
