from __future__ import annotations

from datetime import datetime
from typing import List, Union, Literal, Optional, Type

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import selectinload

from .Common import *
from .. import Models, Schemas
from ..dependencies import get_dependencies, Dependencies
################################################################################

router = APIRouter(prefix="/profiles", tags=["Character Profile Creation"])

################################################################################
def full_profile_manager_select(deps: Dependencies) -> Type[Models.ProfileManagerModel]:

    profile_mgr = deps.db.query(Models.ProfileManagerModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.ProfileManagerModel.requirements),
        selectinload(Models.ProfileManagerModel.channel_groups),
        selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.details),
        selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.ataglance),
        selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.personality),
        selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.images).selectinload(Models.ProfileImagesModel.addl_images),
    ).first()

    if not profile_mgr:
        raise HTTPException(status_code=404, detail="Profile Manager not found for this guild.")

    return profile_mgr

################################################################################
def full_profile_select(
    deps: Dependencies,
    mode: Literal["All", "Single"] = "Single",
    profile_id: Optional[int] = None
):

    query = deps.db.query(Models.ProfileModel).filter_by(guild_id=deps.guild_id).options(
        selectinload(Models.ProfileModel.details),
        selectinload(Models.ProfileModel.ataglance),
        selectinload(Models.ProfileModel.personality),
        selectinload(Models.ProfileModel.images).selectinload(Models.ProfileImagesModel.addl_images),
    )

    if mode == "All":
        return query.all()
    elif mode == "Single":
        assert profile_id is not None
        return query.filter_by(id=profile_id).first()

################################################################################
# GET Requests
################################################################################
@router.get("/", response_model=Schemas.DeepProfileManagerSchema, summary="Get the Profile Manager of the provided guild")
def get_profile_manager(deps: Dependencies = Depends(get_dependencies)) -> Schemas.DeepProfileManagerSchema:

    profile_mgr = full_profile_manager_select(deps)
    return Schemas.DeepProfileManagerSchema.model_validate(profile_mgr)

################################################################################
@router.get("/{profile_id}", response_model=Schemas.DeepProfileSchema, summary="Get a specific Profile by its ID")
def get_profile_by_id(
    profile_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepProfileSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    profile = full_profile_select(deps, mode="Single", profile_id=profile_id)
    return Schemas.DeepProfileSchema.model_validate(profile)

################################################################################
# POST Requests
################################################################################
@router.post("/", status_code=201, response_model=Schemas.DeepProfileSchema, summary="Create a new Profile")
def create_profile(
    data: Schemas.ProfileCreateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepProfileSchema:

    new_profile = Models.ProfileModel(guild_id=deps.guild_id, **data.model_dump())
    deps.db.add(new_profile)
    deps.db.flush()
    deps.db.refresh(new_profile)

    audit_log_create(deps, new_profile, new_profile.id)

    # Create default details, at-a-glance, personality, and images for the new profile
    details = Models.ProfileDetailsModel(profile_id=new_profile.id)
    ataglance = Models.ProfileAtAGlanceModel(profile_id=new_profile.id)
    personality = Models.ProfilePersonalityModel(profile_id=new_profile.id)
    images = Models.ProfileImagesModel(profile_id=new_profile.id)

    deps.db.add_all([details, ataglance, personality, images])
    deps.db.flush()

    profile = full_profile_select(deps, "Single", profile_id=new_profile.id)
    return Schemas.DeepProfileSchema.model_validate(profile)

################################################################################
@router.post("/channel-groups", status_code=201, response_model=Schemas.ProfileChannelGroupSchema, summary="Create a new Profile Channel Group")
def create_profile_channel_group(deps: Dependencies = Depends(get_dependencies)) -> Schemas.ProfileChannelGroupSchema:

    new_group = Models.ProfileChannelGroupModel(guild_id=deps.guild_id)
    deps.db.add(new_group)
    deps.db.flush()
    deps.db.refresh(new_group)

    audit_log_create(deps, new_group, new_group.id)
    return Schemas.ProfileChannelGroupSchema.model_validate(new_group)

################################################################################
@router.post("/{profile_id}/images/additional", status_code=201, response_model=Schemas.ProfileAdditionalImageSchema, summary="Add an additional image to a Profile")
def add_additional_image(
    profile_id: int,
    data: Schemas.ProfileAdditionalImageCreateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileAdditionalImageSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    new_image = Models.ProfileAdditionalImageModel(profile_id=profile.id, **data.model_dump())
    deps.db.add(new_image)
    deps.db.flush()
    deps.db.refresh(new_image)

    audit_log_create(deps, new_image, new_image.profile_id)
    return Schemas.ProfileAdditionalImageSchema.model_validate(new_image)

################################################################################
# DELETE Requests
################################################################################
@router.delete("/{profile_id}", status_code=204, summary="Delete a Profile by its ID")
def delete_profile(
    profile_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    deps.db.delete(profile)
    audit_log_delete(deps, profile, profile.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/channel-groups/{group_id}", status_code=204, summary="Delete a Profile Channel Group by its ID")
def delete_profile_channel_group(
    group_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    group = get_shallow_or_404(deps.db, Models.ProfileChannelGroupModel, id=group_id)
    match_or_403(deps.guild_id, group.guild_id)

    deps.db.delete(group)
    audit_log_delete(deps, group, group.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
@router.delete("/{profile_id}/images/additional/{image_id}", status_code=204, summary="Delete an additional image from a Profile")
def delete_additional_image(
    profile_id: int,
    image_id: int,
    deps: Dependencies = Depends(get_dependencies)
) -> Response:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    image = get_shallow_or_404(deps.db, Models.ProfileAdditionalImageModel, id=image_id)
    match_or_403(profile.id, image.profile_id)

    deps.db.delete(image)
    audit_log_delete(deps, image, image.id)
    deps.db.flush()

    return Response(status_code=204)

################################################################################
# PATCH Requests
################################################################################
@router.patch("/requirements", response_model=Schemas.ProfileRequirementsSchema, summary="Update server Profile Requirements")
def update_profile_requirements(
    data: Schemas.ProfileRequirementsUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileRequirementsSchema:

    requirements = get_shallow_or_404(deps.db, Models.ProfileRequirementsModel, guild_id=deps.guild_id)
    match_or_403(deps.guild_id, requirements.guild_id)

    apply_updates(requirements, data)
    audit_log_update(deps, requirements, requirements.guild_id)

    deps.db.flush()
    deps.db.refresh(requirements)

    return Schemas.ProfileRequirementsSchema.model_validate(requirements)

################################################################################
@router.patch("/channel-groups/{group_id}", response_model=Schemas.ProfileChannelGroupSchema, summary="Update a Profile Channel Group")
def update_profile_channel_group(
    group_id: int,
    data: Schemas.ProfileChannelGroupUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileChannelGroupSchema:

    group = get_shallow_or_404(deps.db, Models.ProfileChannelGroupModel, id=group_id)
    match_or_403(deps.guild_id, group.guild_id)

    apply_updates(group, data)
    audit_log_update(deps, group, group.id)

    deps.db.flush()
    deps.db.refresh(group)

    return Schemas.ProfileChannelGroupSchema.model_validate(group)

################################################################################
@router.patch("/{profile_id}", response_model=Schemas.DeepProfileSchema, summary="Update a Profile's core data.")
def update_profile(
    profile_id: int,
    data: Schemas.ProfileUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.DeepProfileSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    apply_updates(profile, data)
    audit_log_update(deps, profile, profile.id)

    deps.db.flush()
    deps.db.refresh(profile)

    return Schemas.DeepProfileSchema.model_validate(profile)

################################################################################
@router.patch("/{profile_id}/details", response_model=Schemas.ProfileDetailsSchema, summary="Update a Profile's details.")
def update_profile_details(
    profile_id: int,
    data: Schemas.ProfileDetailsUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileDetailsSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    details = get_shallow_or_404(deps.db, Models.ProfileDetailsModel, profile_id=profile.id)

    apply_updates(details, data)
    audit_log_update(deps, details, details.profile_id)

    deps.db.flush()
    deps.db.refresh(details)

    return Schemas.ProfileDetailsSchema.model_validate(details)

################################################################################
@router.patch("/{profile_id}/at-a-glance", response_model=Schemas.ProfileAtAGlanceSchema, summary="Update a Profile's At-A-Glance data.")
def update_profile_at_a_glance(
    profile_id: int,
    data: Schemas.ProfileAtAGlanceUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileAtAGlanceSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    ataglance = get_shallow_or_404(deps.db, Models.ProfileAtAGlanceModel, profile_id=profile.id)

    apply_updates(ataglance, data)
    audit_log_update(deps, ataglance, ataglance.profile_id)

    deps.db.flush()
    deps.db.refresh(ataglance)

    return Schemas.ProfileAtAGlanceSchema.model_validate(ataglance)

################################################################################
@router.patch("/{profile_id}/personality", response_model=Schemas.ProfilePersonalitySchema, summary="Update a Profile's Personality data.")
def update_profile_personality(
    profile_id: int,
    data: Schemas.ProfilePersonalityUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfilePersonalitySchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    personality = get_shallow_or_404(deps.db, Models.ProfilePersonalityModel, profile_id=profile.id)

    apply_updates(personality, data)
    audit_log_update(deps, personality, personality.profile_id)

    deps.db.flush()
    deps.db.refresh(personality)

    return Schemas.ProfilePersonalitySchema.model_validate(personality)

################################################################################
@router.patch("/{profile_id}/images", response_model=Schemas.ProfileImagesSchema, summary="Update a Profile's images.")
def update_profile_images(
    profile_id: int,
    data: Schemas.ProfileImagesUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileImagesSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    images = get_shallow_or_404(deps.db, Models.ProfileImagesModel, profile_id=profile.id)

    apply_updates(images, data)
    audit_log_update(deps, images, images.profile_id)

    deps.db.flush()
    deps.db.refresh(images)

    return Schemas.ProfileImagesSchema.model_validate(images)

################################################################################
@router.patch("/{profile_id}/images/additional/{image_id}", response_model=Schemas.ProfileAdditionalImageSchema, summary="Update an additional image of a Profile")
def update_additional_image(
    profile_id: int,
    image_id: int,
    data: Schemas.ProfileAdditionalImageUpdateSchema,
    deps: Dependencies = Depends(get_dependencies)
) -> Schemas.ProfileAdditionalImageSchema:

    profile = get_shallow_or_404(deps.db, Models.ProfileModel, id=profile_id)
    match_or_403(deps.guild_id, profile.guild_id)

    image = get_shallow_or_404(deps.db, Models.ProfileAdditionalImageModel, id=image_id)
    match_or_403(profile.id, image.profile_id)

    apply_updates(image, data)
    audit_log_update(deps, image, image.id)

    deps.db.flush()
    deps.db.refresh(image)

    return Schemas.ProfileAdditionalImageSchema.model_validate(image)

################################################################################
