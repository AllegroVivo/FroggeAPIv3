from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = (
    "GiveawayManagerModel",
    "GiveawayModel",
    "GiveawayDetailsModel",
    "GiveawayEntryModel",
)

################################################################################
class GiveawayManagerModel(BaseModel):

    __tablename__ = 'giveaway_managers'

    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="giveaways_guild_ids_fkey"), primary_key=True)
    channel_id = Column(BigInteger, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="giveaway_mgr")
    giveaways = relationship("GiveawayModel", back_populates="manager")

################################################################################
class GiveawayModel(BaseModel):

    __tablename__ = 'giveaways'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey("giveaway_managers.guild_id", name="giveaways_giveaway_managers_fkey"), nullable=False)
    winners = Column(ArrayOrJSON(BigInteger), nullable=False, default=[], server_default="[]")
    post_url = Column(String, nullable=True)
    rolled_at = Column(TIMESTAMP, nullable=True)
    rolled_by = Column(BigInteger, nullable=True)

    # Relationships
    manager = relationship("GiveawayManagerModel", back_populates="giveaways")
    details = relationship("GiveawayDetailsModel", back_populates="giveaway", uselist=False, cascade="all, delete-orphan")
    entries = relationship("GiveawayEntryModel", back_populates="giveaway", cascade="all, delete-orphan")

################################################################################
class GiveawayDetailsModel(BaseModel):

    __tablename__ = 'giveaway_details'

    giveaway_id = Column(Integer, ForeignKey("giveaways.id", name="giveaway_details_giveaways_fkey", ondelete="CASCADE"), primary_key=True)
    name = Column(String, nullable=True)
    prize = Column(String, nullable=True)
    num_winners = Column(Integer, nullable=False, default=1, server_default="1")
    auto_notify = Column(NormalizedBoolean, nullable=False, default=True, server_default="True")
    description = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    color = Column(Integer, nullable=True)
    end_dt = Column(TIMESTAMP, nullable=True)
    emoji = Column(String, nullable=True)

    # Relationships
    giveaway = relationship("GiveawayModel", back_populates="details")

################################################################################
class GiveawayEntryModel(BaseModel):

    __tablename__ = 'giveaway_entries'

    id = Column(Integer, primary_key=True)
    giveaway_id = Column(Integer, ForeignKey("giveaways.id", name="giveaway_entries_giveaways_fkey"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relationships
    giveaway = relationship("GiveawayModel", back_populates="entries")

################################################################################
