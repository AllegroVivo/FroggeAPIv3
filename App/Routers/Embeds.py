from __future__ import annotations

from typing import List, Union, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/embeds", tags=["Custom Embed Management"])

################################################################################
def full_embed_select(
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    embed_id: Optional[int] = None
):

    query = deps.db.query(Models.EmbedModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.EmbedModel.images),
        selectinload(Models.EmbedModel.header),
        selectinload(Models.EmbedModel.footer),
        selectinload(Models.EmbedModel.fields)
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert embed_id is not None
        return query.filter_by(id=embed_id).first()

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=List[Schemas.DeepEmbedSchema])
def get_embeds(deps: Dependencies = Depends(get_dependencies)) -> List[Schemas.DeepEmbedSchema]:

    embeds = full_embed_select(deps, "All")
    return [map_embed(embed) for embed in embeds]

################################################################################
@router.get("/{embed_id}", response_model=Schemas.DeepEmbedSchema)
def get_embed(
    embed_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepEmbedSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    embed = full_embed_select(deps, "Single", embed_id=embed.id)
    return map_embed(embed)

################################################################################
@router.get("/{embed_id}/fields/{field_id}", response_model=Schemas.EmbedFieldSchema)
def get_embed_field(
    embed_id: int,
    field_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.EmbedFieldSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    field = get_shallow_or_404(deps.db, Models.EmbedFieldModel, id=field_id)
    match_or_403(embed.id, field.embed_id)

    return Schemas.EmbedFieldSchema.model_validate(field)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.DeepEmbedSchema)
def create_embed(
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepEmbedSchema:

    new_embed = Models.EmbedModel(guild_id=deps.guild_id)
    deps.db.add(new_embed)
    deps.db.flush()

    audit_log_create(deps, new_embed, new_embed.id)

    deps.db.add_all([
        Models.EmbedImagesModel(embed_id=new_embed.id),
        Models.EmbedHeaderModel(embed_id=new_embed.id),
        Models.EmbedFooterModel(embed_id=new_embed.id)
    ])
    deps.db.flush()

    created = full_embed_select(deps, "Single", embed_id=new_embed.id)
    return map_embed(created)

################################################################################
@router.post("/{embed_id}/fields", status_code=201, response_model=Schemas.EmbedFieldSchema)
def create_embed_field(
    embed_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.EmbedFieldSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    current_fields = deps.db.query(Models.EmbedFieldModel).filter(Models.EmbedFieldModel.embed_id == embed.id).all()
    current_fields.sort(key=lambda x: x.sort_order)

    sort_order = next_sort_order(current_fields)

    new_field = Models.EmbedFieldModel(embed_id=embed.id, sort_order=sort_order)

    deps.db.add(new_field)
    deps.db.flush()
    deps.db.refresh(new_field)

    audit_log_create(deps, new_field, new_field.id)
    return Schemas.EmbedFieldSchema.model_validate(new_field)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{embed_id}", status_code=204)
def delete_embed(embed_id: int, deps: Dependencies = Depends(get_dependencies)) -> Response:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    deps.db.delete(embed)
    audit_log_delete(deps, embed, deps.actor_id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{embed_id}/fields/{field_id}", status_code=204)
def delete_embed_field(
    embed_id: int,
    field_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    field = get_shallow_or_404(deps.db, Models.EmbedFieldModel, id=field_id)
    match_or_403(embed.id, field.embed_id)

    deps.db.delete(field)
    audit_log_delete(deps, field, deps.actor_id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/{embed_id}", response_model=Schemas.DeepEmbedSchema)
def patch_embed(
    embed_id: int,
    data: Schemas.EmbedUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepEmbedSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    apply_updates(embed, data)
    audit_log_update(deps, embed, embed.id)

    deps.db.flush()
    deps.db.refresh(embed)

    embed = full_embed_select(deps, "Single", embed_id=embed.id)
    return map_embed(embed)

################################################################################
@router.patch("/{embed_id}/images", response_model=Schemas.EmbedImagesSchema)
def patch_embed_images(
    embed_id: int,
    data: Schemas.EmbedImagesUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.EmbedImagesSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    images = get_shallow_or_404(deps.db, Models.EmbedImagesModel, embed_id=embed_id)
    match_or_403(embed.id, images.embed_id)

    apply_updates(images, data)
    audit_log_update(deps, images, embed.id)

    deps.db.flush()
    deps.db.refresh(images)

    return Schemas.EmbedImagesSchema.model_validate(images)

################################################################################
@router.patch("/{embed_id}/header", response_model=Schemas.EmbedHeaderSchema)
def patch_embed_header(
    embed_id: int,
    data: Schemas.EmbedHeaderUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.EmbedHeaderSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    header = get_shallow_or_404(deps.db, Models.EmbedHeaderModel, embed_id=embed_id)
    match_or_403(embed.id, header.embed_id)

    apply_updates(header, data)
    audit_log_update(deps, header, embed.id)

    deps.db.flush()
    deps.db.refresh(header)

    return Schemas.EmbedHeaderSchema.model_validate(header)

################################################################################
@router.patch("/{embed_id}/footer", response_model=Schemas.EmbedFooterSchema)
def patch_embed_footer(
    embed_id: int,
    data: Schemas.EmbedFooterUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.EmbedFooterSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    footer = get_shallow_or_404(deps.db, Models.EmbedFooterModel, embed_id=embed_id)
    match_or_403(embed.id, footer.embed_id)

    apply_updates(footer, data)
    audit_log_update(deps, footer, embed.id)

    deps.db.flush()
    deps.db.refresh(footer)

    return Schemas.EmbedFooterSchema.model_validate(footer)

################################################################################
@router.patch("/{embed_id}/fields/{field_id}", response_model=Schemas.EmbedFieldSchema)
def patch_embed_field(
    embed_id: int,
    field_id: int,
    data: Schemas.EmbedFieldUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.EmbedFieldSchema:

    embed = get_shallow_or_404(deps.db, Models.EmbedModel, id=embed_id)
    match_or_403(deps.guild_id, embed.guild_id)

    field = get_shallow_or_404(deps.db, Models.EmbedFieldModel, id=field_id)
    match_or_403(embed.id, field.embed_id)

    if data.sort_order is not None:
        exists = deps.db.query(Models.EmbedFieldModel).filter_by(embed_id=embed_id, sort_order=data.sort_order).first()
        if exists and exists.id != field_id:
            raise HTTPException(status_code=409, detail=f"Sort order {data.sort_order} already exists for another field in this embed")

    apply_updates(field, data)
    audit_log_update(deps, field, embed.id)

    deps.db.flush()
    deps.db.refresh(field)

    return Schemas.EmbedFieldSchema.model_validate(field)

################################################################################
