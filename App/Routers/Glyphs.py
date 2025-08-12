from __future__ import annotations

from typing import List, Union, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/glyph-messages", tags=["Customizable PF Glyph Messages"])

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=List[Schemas.GlyphMessageSchema], summary="Get all Glyph Messages for the guild")
async def get_glyph_messages(deps: Dependencies = Depends(get_dependencies)) -> List[Schemas.GlyphMessageSchema]:

    messages = deps.db.query(Models.GlyphMessageModel).filter_by(guild_id=deps.guild_id).all()
    return [Schemas.GlyphMessageSchema.model_validate(msg) for msg in messages]

################################################################################
@router.get("/{glyph_message_id}", response_model=Schemas.GlyphMessageSchema, summary="Get a specific Glyph Message by its ID")
async def get_glyph_message(
    glyph_message_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.GlyphMessageSchema:

    glyph_message = get_shallow_or_404(deps.db, Models.GlyphMessageModel, id=glyph_message_id)
    match_or_403(deps.guild_id, glyph_message.guild_id)

    return Schemas.GlyphMessageSchema.model_validate(glyph_message)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.GlyphMessageSchema, summary="Create a new Glyph Message")
def create_glyph_message(deps: Dependencies = Depends(get_dependencies)) -> Schemas.GlyphMessageSchema:

    new_message = Models.GlyphMessageModel(guild_id=deps.guild_id)
    deps.db.add(new_message)
    deps.db.flush()
    deps.db.refresh(new_message)

    audit_log_create(deps, new_message, new_message.id)
    return Schemas.GlyphMessageSchema.model_validate(new_message)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{glyph_message_id}", status_code=204, summary="Delete a Glyph Message by its ID")
def delete_glyph_message(
    glyph_message_id: int,
    deps: Dependencies = Depends(get_dependencies)
):

    message = get_shallow_or_404(deps.db, Models.GlyphMessageModel, id=glyph_message_id)

    deps.db.delete(message)
    audit_log_delete(deps, message, message.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/{glyph_message_id}", response_model=Schemas.GlyphMessageSchema, summary="Update a Glyph Message by its ID")
def update_glyph_message(
    glyph_message_id: int,
    data: Schemas.GlyphMessageUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.GlyphMessageSchema:

    message = get_shallow_or_404(deps.db, Models.GlyphMessageModel, id=glyph_message_id)

    apply_updates(message, data)
    audit_log_update(deps, message, message.id)

    deps.db.flush()
    deps.db.refresh(message)

    return Schemas.GlyphMessageSchema.model_validate(message)

################################################################################
