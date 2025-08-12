from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, func, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = (
    "RaffleManagerModel",
    "RaffleModel",
    "RaffleEntryModel",
)

################################################################################
class RaffleManagerModel(BaseModel):

    __tablename__ = 'raffle_managers'

    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="raffle_managers_guild_ids_fkey"), primary_key=True)
    channel_id = Column(BigInteger, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="raffle_mgr")
    raffles = relationship("RaffleModel", back_populates="manager")

################################################################################
class RaffleModel(BaseModel):

    __tablename__ = 'raffles'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("raffle_managers.guild_id", name="raffles_raffle_managers_fkey"), nullable=False)
    winners = Column(ArrayOrJSON(BigInteger), nullable=False, default="[]", server_default="{}")
    is_active = Column(NormalizedBoolean, nullable=False, default=False, server_default="false")
    post_url = Column(String, nullable=True)
    name = Column(String, nullable=True)
    prize = Column(String, nullable=True)
    num_winners = Column(Integer, nullable=False, default=1, server_default="1")
    auto_notify = Column(NormalizedBoolean, nullable=False, default=True, server_default="True")
    cost = Column(Integer, nullable=False, default=100000, server_default="100000")

    rolled_at = Column(TIMESTAMP, nullable=True)
    rolled_by = Column(BigInteger, nullable=True)

    # Relationships
    manager = relationship("RaffleManagerModel", back_populates="raffles")
    entries = relationship("RaffleEntryModel", back_populates="raffle", cascade="all, delete-orphan")

################################################################################
class RaffleEntryModel(BaseModel):

    __tablename__ = 'raffle_entries'

    id = Column(Integer, primary_key=True)
    raffle_id = Column(Integer, ForeignKey("raffles.id", name="raffle_entries_raffles_fkey"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, nullable=False, default=1, server_default="1")

    # Relationships
    raffle = relationship("RaffleModel", back_populates="entries")

################################################################################
