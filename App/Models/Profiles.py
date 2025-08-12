from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, VARCHAR, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = (
    "ProfileManagerModel",
    "ProfileRequirementsModel",
    "ProfileModel",
    "ProfileImagesModel",
    "ProfileAtAGlanceModel",
    "ProfilePersonalityModel",
    "ProfileDetailsModel",
    "ProfileAdditionalImageModel",
    "ProfileChannelGroupModel",
)

################################################################################
class ProfileManagerModel(BaseModel):

    __tablename__ = 'profile_managers'

    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="profile_managers_guild_ids_fkey"), primary_key=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="profile_mgr")
    requirements = relationship("ProfileRequirementsModel", back_populates="manager", uselist=False)
    profiles = relationship("ProfileModel", back_populates="manager")
    channel_groups = relationship("ProfileChannelGroupModel", back_populates="guild")

################################################################################
class ProfileRequirementsModel(BaseModel):

    __tablename__ = 'profile_requirements'

    guild_id = Column(BigInteger, ForeignKey("profile_managers.guild_id", name="profile_requirements_profile_managers_fkey"), primary_key=True)
    url = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    color = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    jobs = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    rates = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    gender = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    race = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    orientation = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    height = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    age = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    mare = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    world = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    likes = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    dislikes = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    personality = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    aboutme = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    thumbnail = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    main_image = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")

    # Relationships
    manager = relationship("ProfileManagerModel", back_populates="requirements")

################################################################################
class ProfileModel(BaseModel):

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    guild_id = Column(BigInteger, ForeignKey("profile_managers.guild_id", name="profiles_profile_managers_fkey"), nullable=False)
    post_url = Column(String, nullable=True)

    # Relationships
    manager = relationship("ProfileManagerModel", back_populates="profiles")
    images = relationship("ProfileImagesModel", back_populates="profile", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    ataglance = relationship("ProfileAtAGlanceModel", back_populates="profile", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    details = relationship("ProfileDetailsModel", back_populates="profile", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    personality = relationship("ProfilePersonalityModel", back_populates="profile", uselist=False, cascade="all, delete-orphan", passive_deletes=True)

################################################################################
class ProfileImagesModel(BaseModel):

    __tablename__ = 'profile_images'

    profile_id = Column(Integer, ForeignKey("profiles.id", name="profile_images_profiles_fkey", ondelete="CASCADE"), primary_key=True)
    thumbnail_url = Column(String, nullable=True)
    main_image_url = Column(String, nullable=True)

    # Relationships
    profile = relationship("ProfileModel", back_populates="images")
    addl_images = relationship("ProfileAdditionalImageModel", back_populates="parent", cascade="all, delete-orphan", passive_deletes=True)

################################################################################
class ProfileAtAGlanceModel(BaseModel):

    __tablename__ = 'profile_at_a_glances'

    profile_id = Column(Integer, ForeignKey("profiles.id", name="profile_at_a_glance_profiles_fkey", ondelete="CASCADE"), primary_key=True)
    world = Column(Integer, nullable=True)
    gender_enum = Column(Integer, nullable=True)
    pronouns = Column(ArrayOrJSON(Integer), nullable=False, default=[], server_default="[]")
    race_enum = Column(Integer, nullable=True)
    clan_enum = Column(Integer, nullable=True)
    orientation_enum = Column(Integer, nullable=True)
    race_custom = Column(String, nullable=True)
    clan_custom = Column(String, nullable=True)
    orientation_custom = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    age = Column(String, nullable=True)
    mare = Column(String, nullable=True)

    # Relationships
    profile = relationship("ProfileModel", back_populates="ataglance")

################################################################################
class ProfilePersonalityModel(BaseModel):

    __tablename__ = 'profile_personalities'

    profile_id = Column(Integer, ForeignKey("profiles.id", name="profile_personalities_profiles_fkey", ondelete="CASCADE"), primary_key=True)
    likes = Column(ArrayOrJSON(String), nullable=True)
    dislikes = Column(ArrayOrJSON(String), nullable=True)
    personality = Column(String, nullable=True)
    aboutme = Column(String, nullable=True)

    # Relationships
    profile = relationship("ProfileModel", back_populates="personality")

################################################################################
class ProfileDetailsModel(BaseModel):

    __tablename__ = 'profile_details'

    profile_id = Column(Integer, ForeignKey("profiles.id", name="profile_details_profiles_fkey", ondelete="CASCADE"), primary_key=True)
    name = Column(String, nullable=True)
    custom_url = Column(String, nullable=True)
    color = Column(Integer, nullable=True)
    jobs = Column(ArrayOrJSON, nullable=False, default=[], server_default="[]")
    rates = Column(String, nullable=True)

    # Relationships
    profile = relationship("ProfileModel", back_populates="details")

################################################################################
class ProfileAdditionalImageModel(BaseModel):

    __tablename__ = 'profile_additional_images'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile_images.profile_id", name="profile_additional_images_profile_images_fkey", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    caption = Column(String, nullable=True)

    # Relationships
    parent = relationship("ProfileImagesModel", back_populates="addl_images")

################################################################################
class ProfileChannelGroupModel(BaseModel):

    __tablename__ = 'profile_channel_groups'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("profile_managers.guild_id", name="profile_channel_groups_profile_managers_fkey"), nullable=False)
    channel_ids = Column(ArrayOrJSON(BigInteger), nullable=False, default=[], server_default="[]")
    role_ids = Column(ArrayOrJSON(BigInteger), nullable=False, default=[], server_default="[]")

    # Relationships
    guild = relationship("ProfileManagerModel", back_populates="channel_groups")

################################################################################
