from __future__ import annotations

from sqlalchemy import Column, Integer, JSON, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .Common import BaseModel
################################################################################

__all__ = ("GlyphMessageModel",)

################################################################################
class GlyphMessageModel(BaseModel):

    __tablename__ = 'glyph_messages'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="glyph_messages_guild_ids_fkey"), nullable=False)
    name = Column(String, nullable=True)
    message = Column(JSON, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="glyph_msgs")

################################################################################
