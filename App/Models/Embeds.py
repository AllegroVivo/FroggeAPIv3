from __future__ import annotations

from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP, text, UniqueConstraint
from sqlalchemy.orm import relationship

from .Common import BaseModel, NormalizedBoolean
################################################################################

__all__ = (
    "EmbedModel",
    "EmbedImagesModel",
    "EmbedHeaderModel",
    "EmbedFooterModel",
    "EmbedFieldModel",
)

################################################################################
class EmbedModel(BaseModel):

    __tablename__ = 'embeds'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="embeds_guild_ids_fkey"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    color = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="embeds")
    images = relationship("EmbedImagesModel", back_populates="embed", cascade="all, delete-orphan", passive_deletes=True, uselist=False)
    header = relationship("EmbedHeaderModel", back_populates="embed", cascade="all, delete-orphan", passive_deletes=True, uselist=False)
    footer = relationship("EmbedFooterModel", back_populates="embed", cascade="all, delete-orphan", passive_deletes=True, uselist=False)
    fields = relationship("EmbedFieldModel", back_populates="embed", cascade="all, delete-orphan", passive_deletes=True)

################################################################################
class EmbedImagesModel(BaseModel):

    __tablename__ = 'embed_images'

    embed_id = Column(Integer, ForeignKey("embeds.id", name="embed_images_embeds_fkey", ondelete="CASCADE"), primary_key=True)
    thumbnail_url = Column(String, nullable=True)
    main_image_url = Column(String, nullable=True)

    # Relationships
    embed = relationship("EmbedModel", back_populates="images", passive_deletes=True)

################################################################################
class EmbedHeaderModel(BaseModel):

    __tablename__ = 'embed_headers'

    embed_id = Column(Integer, ForeignKey("embeds.id", name="embed_headers_embeds_fkey", ondelete="CASCADE"), primary_key=True)
    text = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)
    url = Column(String, nullable=True)

    # Relationships
    embed = relationship("EmbedModel", back_populates="header", passive_deletes=True)

################################################################################
class EmbedFooterModel(BaseModel):

    __tablename__ = 'embed_footers'

    embed_id = Column(Integer, ForeignKey("embeds.id", name="embed_footers_embeds_fkey", ondelete="CASCADE"), primary_key=True)
    text = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)

    # Relationships
    embed = relationship("EmbedModel", back_populates="footer", passive_deletes=True)

################################################################################
class EmbedFieldModel(BaseModel):

    __tablename__ = 'embed_fields'

    id = Column(Integer, primary_key=True)
    embed_id = Column(Integer, ForeignKey("embeds.id", name="embed_fields_embeds_fkey", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=True)
    value = Column(String, nullable=True)
    inline = Column(NormalizedBoolean, nullable=False, default=False, server_default=text("false"))
    sort_order = Column(Integer, nullable=False)

    # Relationships
    embed = relationship("EmbedModel", back_populates="fields", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('embed_id', 'sort_order', name='uq_embed_field_sort_order'),
    )

################################################################################
