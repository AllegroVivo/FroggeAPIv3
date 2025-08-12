from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = ("PositionModel",)

################################################################################
class PositionModel(BaseModel):

    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="positions_guild_ids_fkey"), nullable=False)
    name = Column(String, nullable=True)
    role_id = Column(BigInteger, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="positions")
    # events = relationship("EventPositionModel", back_populates="position")

################################################################################
