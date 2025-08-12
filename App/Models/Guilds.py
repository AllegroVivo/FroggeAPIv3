from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = ("GuildIDModel", "GuildConfigurationModel")

################################################################################
class GuildIDModel(BaseModel):

    __tablename__ = "guild_ids"

    guild_id = Column(BigInteger, primary_key=True)

    # Relationships
    configuration = relationship("GuildConfigurationModel", back_populates="guild", uselist=False)
    embeds = relationship("EmbedModel", back_populates="guild")
    # event_mgr = relationship("EventManagerModel", back_populates="guild", uselist=False)
    forms = relationship("FormModel", back_populates="guild")
    giveaway_mgr = relationship("GiveawayManagerModel", back_populates="guild", uselist=False)
    glyph_msgs = relationship("GlyphMessageModel", back_populates="guild")
    positions = relationship("PositionModel", back_populates="guild")
    profile_mgr = relationship("ProfileManagerModel", back_populates="guild", uselist=False)
    raffle_mgr = relationship("RaffleManagerModel", back_populates="guild", uselist=False)
    role_mgr = relationship("ReactionRoleManagerModel", back_populates="guild", uselist=False)
    # staff_mgr = relationship("StaffManagerModel", back_populates="guild", uselist=False)
    # room_mgr = relationship("RoomManagerModel", back_populates="guild", uselist=False)
    # vip_mgr = relationship("VIPManagerModel", back_populates="guild", uselist=False)

################################################################################
class GuildConfigurationModel(BaseModel):

    __tablename__ = "guild_configurations"

    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id"), primary_key=True)
    timezone = Column(Integer, nullable=False, server_default="7")
    log_channel_id = Column(BigInteger, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="configuration")

################################################################################
