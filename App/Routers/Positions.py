from __future__ import annotations

from typing import List, Union, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/positions", tags=["Staffable Position Management"])

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=List[Schemas.PositionSchema], summary="Get all Positions for the guild")
async def get_glyph_messages(deps: Dependencies = Depends(get_dependencies)) -> List[Schemas.PositionSchema]:

    positions = deps.db.query(Models.PositionModel).filter_by(guild_id=deps.guild_id).all()
    return [Schemas.PositionSchema.model_validate(pos) for pos in positions]

################################################################################
@router.get("/{position_id}", response_model=Schemas.PositionSchema, summary="Get a specific Position by its ID")
async def get_glyph_message(
    position_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.PositionSchema:

    position = get_shallow_or_404(deps.db, Models.PositionModel, id=position_id)
    return Schemas.PositionSchema.model_validate(position)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.PositionSchema, summary="Create a new Position")
def create_glyph_message(deps: Dependencies = Depends(get_dependencies)) -> Schemas.PositionSchema:

    position = Models.PositionModel(guild_id=deps.guild_id)
    deps.db.add(position)
    deps.db.flush()
    deps.db.refresh(position)

    audit_log_create(deps, position, position.id)
    return Schemas.PositionSchema.model_validate(position)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{position_id}", status_code=204, summary="Delete a Position by its ID")
def delete_glyph_message(
    position_id: int,
    deps: Dependencies = Depends(get_dependencies)
):

    position = get_shallow_or_404(deps.db, Models.PositionModel, id=position_id)

    deps.db.delete(position)
    audit_log_delete(deps, position, position.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/{position_id}", response_model=Schemas.PositionSchema, summary="Update a Position by its ID")
def update_glyph_message(
    position_id: int,
    data: Schemas.PositionUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.PositionSchema:

    position = get_shallow_or_404(deps.db, Models.PositionModel, id=position_id)

    apply_updates(position, data)
    audit_log_update(deps, position, position.id)

    deps.db.flush()
    deps.db.refresh(position)

    return Schemas.PositionSchema.model_validate(position)

################################################################################
