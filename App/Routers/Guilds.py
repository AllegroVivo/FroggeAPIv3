from __future__ import annotations

from typing import Literal, Optional, Type

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from .Common import *
from App import Models, Schemas
from App.dependencies import get_dependencies, Dependencies, get_db
################################################################################

router = APIRouter(prefix="", tags=["Guild Endpoints"])

################################################################################
# Helper Functions
################################################################################
def full_guild_select(db: Session, mode: Literal["All", "First"] = "All", guild_id: Optional[int] = None):

    query = db.query(Models.GuildIDModel).options(
        selectinload(Models.GuildIDModel.configuration),
        selectinload(Models.GuildIDModel.embeds).selectinload(Models.EmbedModel.images),
        selectinload(Models.GuildIDModel.embeds).selectinload(Models.EmbedModel.header),
        selectinload(Models.GuildIDModel.embeds).selectinload(Models.EmbedModel.footer),
        selectinload(Models.GuildIDModel.embeds).selectinload(Models.EmbedModel.fields),
        # selectinload(Models.GuildIDModel.event_mgr).selectinload(Models.EventManagerModel.events).selectinload(Models.EventModel.positions),
        # selectinload(Models.GuildIDModel.event_mgr).selectinload(Models.EventManagerModel.events).selectinload(Models.EventModel.elements),
        # selectinload(Models.GuildIDModel.event_mgr).selectinload(Models.EventManagerModel.events).selectinload(Models.EventModel.shifts).selectinload(Models.EventShiftBracketModel.signups),
        # selectinload(Models.GuildIDModel.event_mgr).selectinload(Models.EventManagerModel.templates),
        # selectinload(Models.GuildIDModel.forms).selectinload(Models.FormModel.questions).selectinload(Models.FormQuestionModel.responses),
        # selectinload(Models.GuildIDModel.forms).selectinload(Models.FormModel.questions).selectinload(Models.FormQuestionModel.options),
        # selectinload(Models.GuildIDModel.forms).selectinload(Models.FormModel.questions).selectinload(Models.FormQuestionModel.prompts),
        # selectinload(Models.GuildIDModel.forms).selectinload(Models.FormModel.response_collections),
        # selectinload(Models.GuildIDModel.forms).selectinload(Models.FormModel.prompts),
        # selectinload(Models.GuildIDModel.forms).selectinload(Models.FormModel.post_options),
        # selectinload(Models.GuildIDModel.giveaway_mgr).selectinload(Models.GiveawayManagerModel.giveaways).selectinload(Models.GiveawayModel.details),
        # selectinload(Models.GuildIDModel.giveaway_mgr).selectinload(Models.GiveawayManagerModel.giveaways).selectinload(Models.GiveawayModel.entries),
        # selectinload(Models.GuildIDModel.glyph_msgs),
        # selectinload(Models.GuildIDModel.profile_mgr).selectinload(Models.ProfileManagerModel.requirements),
        # selectinload(Models.GuildIDModel.profile_mgr).selectinload(Models.ProfileManagerModel.channel_groups),
        # selectinload(Models.GuildIDModel.profile_mgr).selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.details),
        # selectinload(Models.GuildIDModel.profile_mgr).selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.ataglance),
        # selectinload(Models.GuildIDModel.profile_mgr).selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.personality),
        # selectinload(Models.GuildIDModel.profile_mgr).selectinload(Models.ProfileManagerModel.profiles).selectinload(Models.ProfileModel.images).selectinload(Models.ProfileImagesModel.addl_images),
        # selectinload(Models.GuildIDModel.raffle_mgr).selectinload(Models.RaffleManagerModel.raffles).selectinload(Models.RaffleModel.entries),
        # selectinload(Models.GuildIDModel.role_mgr).selectinload(Models.ReactionRoleManagerModel.messages).selectinload(Models.ReactionRoleMessageModel.roles),
        # selectinload(Models.GuildIDModel.room_mgr).selectinload(Models.RoomManagerModel.rooms),
        # selectinload(Models.GuildIDModel.staff_mgr).selectinload(Models.StaffManagerModel.staff).selectinload(Models.StaffMemberModel.employment_dates),
        # selectinload(Models.GuildIDModel.staff_mgr).selectinload(Models.StaffManagerModel.staff).selectinload(Models.StaffMemberModel.characters),
        # selectinload(Models.GuildIDModel.vip_mgr).selectinload(Models.VIPManagerModel.warning_message),
        # selectinload(Models.GuildIDModel.vip_mgr).selectinload(Models.VIPManagerModel.expiry_message),
        # selectinload(Models.GuildIDModel.vip_mgr).selectinload(Models.VIPManagerModel.tiers).selectinload(Models.VIPTierModel.perks),
        # selectinload(Models.GuildIDModel.vip_mgr).selectinload(Models.VIPManagerModel.members).selectinload(Models.VIPMemberModel.overrides),
        # selectinload(Models.GuildIDModel.vip_mgr).selectinload(Models.VIPManagerModel.members).selectinload(Models.VIPMemberModel.memberships),
    )

    if mode == "All":
        return query.all()
    elif mode == "First":
        assert guild_id is not None, "Guild ID must be provided in 'First' mode"
        return query.filter_by(guild_id=guild_id).first()

################################################################################
def full_guild_validate(guild: Type[Models.GuildIDModel]) -> Schemas.GuildDataSchema:

    return Schemas.GuildDataSchema(
        configuration=Schemas.GuildConfigurationSchema.model_validate(guild.configuration),
        embeds=[map_embed(embed) for embed in guild.embeds],
        # event_mgr=Schemas.EventManagerSchema.model_validate(
        #     guild.event_mgr,
        #     context={
        #         "events": [map_event(ev) for ev in guild.event_mgr.events],
        #         "templates": map_schemas(Schemas.EventTemplateSchema, guild.event_mgr.templates),
        #     }
        # ),
        # forms=[map_form(form) for form in guild.forms],
        # giveaway_mgr=Schemas.GiveawayManagerSchema.model_validate(
        #     guild.giveaway_mgr,
        #     context={
        #         "giveaways": [map_giveaway(ga) for ga in guild.giveaway_mgr.giveaways],
        #     }
        # ),
        # glyph_messages=map_schemas(Schemas.GlyphMessageSchema, guild.glyph_msgs),
        # positions=map_schemas(Schemas.DeepPositionSchema, guild.positions),
        # profile_mgr=Schemas.ProfileManagerSchema.model_validate(
        #     guild.profile_mgr,
        #     context={
        #         "requirements": Schemas.ProfileRequirementsSchema.model_validate(guild.profile_mgr.requirements),
        #         "channel_groups": map_schemas(Schemas.ProfileChannelGroupSchema, guild.profile_mgr.channel_groups),
        #         "profiles": [map_profile(p) for p in guild.profile_mgr.profiles]
        #     }
        # ),
        # raffle_mgr=Schemas.RaffleManagerSchema.model_validate(
        #     guild.raffle_mgr,
        #     context={
        #         "raffles": [map_raffle(raffle) for raffle in guild.raffle_mgr.raffles],
        #     }
        # ),
        # reaction_roles_mgr=Schemas.ReactionRoleManagerSchema.model_validate(
        #     guild.role_mgr,
        #     context={
        #         "messages": [map_reaction_role_message(msg) for msg in guild.role_mgr.messages],
        #     }
        # ),
        # room_mgr=Schemas.RoomManagerSchema.model_validate(
        #     guild.room_mgr,
        #     context={
        #         "rooms": map_schemas(Schemas.RoomSchema, guild.room_mgr.rooms),
        #     }
        # ),
        # staff_mgr=Schemas.StaffManagerSchema.model_validate(
        #     guild.staff_mgr,
        #     context={
        #         "staff": [map_staff_member(member) for member in guild.staff_mgr.staff],
        #     }
        # ),
        # vip_mgr=Schemas.VIPManagerSchema.model_validate(
        #     guild.vip_mgr,
        #     context={
        #         "warning_message": Schemas.VIPMessageSchema.model_validate(guild.vip_mgr.warning_message),
        #         "expiry_message": Schemas.VIPMessageSchema.model_validate(guild.vip_mgr.expiry_message),
        #         "tiers": [map_vip_tier(t) for t in guild.vip_mgr.tiers],
        #         "members": [map_vip_member(m) for m in guild.vip_mgr.members]
        #     }
        # )
    )

################################################################################
# GET Requests
################################################################################
@router.get("/guilds/{guild_id}", response_model=Schemas.TopLevelGuildSchema)
def get_single_guild(
    guild_id: int,
    db: Session = Depends(get_db)
) -> Schemas.TopLevelGuildSchema:

    guild = full_guild_select(db, "First", guild_id=guild_id)
    if guild is None:
        raise HTTPException(status_code=404, detail=f"Guild ID '{guild_id}' not found")

    return Schemas.TopLevelGuildSchema(
        guild_id=guild.guild_id,
        data=full_guild_validate(guild)
    )

################################################################################
# POST Requests
################################################################################
@router.post("/guilds", status_code=201, response_model=Schemas.TopLevelGuildSchema)
def create_guild(
    data: Schemas.GuildIDSchema,
    db: Session = Depends(get_db)
) -> Schemas.TopLevelGuildSchema:

    gid = data.guild_id
    guild = db.query(Models.GuildIDModel).filter(Models.GuildIDModel.guild_id == gid).first()
    if guild is not None:
        raise HTTPException(status_code=409, detail=f"Guild ID '{gid}' already exists")

    id_model = Models.GuildIDModel(guild_id=gid)
    config = Models.GuildConfigurationModel(guild_id=gid)
    # event_mgr = Models.EventManagerModel(guild_id=gid)
    giveaway_mgr = Models.GiveawayManagerModel(guild_id=gid)
    profile_mgr = Models.ProfileManagerModel(guild_id=gid)
    profile_reqs = Models.ProfileRequirementsModel(guild_id=gid)
    raffle_mgr = Models.RaffleManagerModel(guild_id=gid)
    reaction_role_mgr = Models.ReactionRoleManagerModel(guild_id=gid)
    # rooms_mgr = Models.RoomManagerModel(guild_id=gid)
    # staff_mgr = Models.StaffManagerModel(guild_id=gid)
    # vip_mgr = Models.VIPManagerModel(guild_id=gid)
    # vip_warning_msg = Models.VIPWarningMessageModel(guild_id=gid)
    # vip_expiry_msg = Models.VIPExpiryMessageModel(guild_id=gid)

    db.add_all([id_model, config, giveaway_mgr, profile_mgr, profile_reqs,
                raffle_mgr, reaction_role_mgr])
    db.flush()

    guild = full_guild_select(db, "First", guild_id=gid)
    if guild is None:
        raise HTTPException(status_code=500, detail="Failed to create guild data")

    return Schemas.TopLevelGuildSchema(
        guild_id=id_model.guild_id,
        data=full_guild_validate(guild)
    )

################################################################################
# PATCH Requests
################################################################################
@router.patch("/guilds/{guild_id}/configuration", response_model=Schemas.GuildConfigurationSchema)
def patch_guild_config(
    guild_id: int,
    data: Schemas.GuildConfigurationUpdateSchema,
    db: Session = Depends(get_db)
) -> Schemas.GuildConfigurationSchema:

    existing = get_shallow_or_404(db, Models.GuildConfigurationModel, guild_id=guild_id)

    apply_updates(existing, data)
    action = Models.AuditLogModel(
        guild_id=guild_id,
        target=existing.__class__.__name__.rstrip("Model"),
        target_id=existing.guild_id,
        action="Update",
        user_id=data.editor_id,
        changes=build_audit_log_changes(existing),
        request_id=None
    )
    db.add(action)

    db.flush()
    db.refresh(existing)

    return Schemas.GuildConfigurationSchema.model_validate(existing)

################################################################################
