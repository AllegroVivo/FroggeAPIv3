from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from pydantic import Field
from App import limits

from .Common import *
################################################################################

__all__ = (
    "BaseEmbedSchema",
    "DeepEmbedSchema",
    "EmbedImagesSchema",
    "EmbedHeaderSchema",
    "EmbedFooterSchema",
    "EmbedFieldSchema",
    "EmbedUpdateSchema",
    "EmbedImagesUpdateSchema",
    "EmbedHeaderUpdateSchema",
    "EmbedFooterUpdateSchema",
    "EmbedFieldUpdateSchema",
)

################################################################################
class BaseEmbedSchema(IdentifiableSchema):
    """
    Base schema for embeds, containing common fields that all embeds should have.
    """

    title: Optional[str] = Field(..., description="Title of the embed")
    description: Optional[str] = Field(..., description="Body of the embed",)
    color: Optional[int] = Field(..., ge=0, le=0xFFFFFF, description="Accent color of the embed")
    url: Optional[str] = Field(..., description="The URL that the embed's title links to")
    timestamp: Optional[datetime] = Field(..., description="Timestamp of the embed, in ISO 8601 format")

################################################################################
class DeepEmbedSchema(BaseEmbedSchema):
    """
    Schema for a deep embed, which includes additional fields.
    """

    images: EmbedImagesSchema = Field(..., description="Images associated with the embed")
    header: EmbedHeaderSchema = Field(..., description="Header of the embed")
    footer: EmbedFooterSchema = Field(..., description="Footer of the embed")
    fields: List[EmbedFieldSchema] = Field(..., description="List of fields in the embed")

################################################################################
class EmbedImagesSchema(BaseSchema):
    """
    Schema for images associated with an embed.
    """

    thumbnail_url: Optional[str] = Field(..., description="URL of the thumbnail image for the embed")
    main_image_url: Optional[str] = Field(..., description="URL of the main image for the embed")

################################################################################
class EmbedHeaderSchema(BaseSchema):
    """
    Schema for the header of an embed.
    """

    text: Optional[str] = Field(..., description="Text for the header of the embed")
    icon_url: Optional[str] = Field(..., description="URL of the icon for the header of the embed")
    url: Optional[str] = Field(..., description="URL that the header links to, if applicable")

################################################################################
class EmbedFooterSchema(BaseSchema):
    """
    Schema for the footer of an embed.
    """

    text: Optional[str] = Field(..., description="Text for the footer of the embed")
    icon_url: Optional[str] = Field(..., description="URL of the icon for the footer of the embed")

################################################################################
class EmbedFieldSchema(IdentifiableSchema):
    """
    Schema for a field in an embed.
    """

    name: Optional[str] = Field(..., description="Name of the field in the embed")
    value: Optional[str] = Field(..., description="Value of the field in the embed")
    inline: bool = Field(..., description="Whether the field should be displayed inline with other fields")
    sort_order: int = Field(..., description="Sort order of the field in the embed, used for ordering purposes")

################################################################################
class EmbedUpdateSchema(BaseSchema):
    """
    Schema for updating an embed, allowing partial updates to its properties.
    """

    title: Optional[str] = Field(None, max_length=limits.EMBED_TITLE_MAX, description="Title of the embed")
    color: Optional[int] = Field(None, ge=0, le=0xFFFFFF, description="Accent color of the embed")
    description: Optional[str] = Field(None, max_length=limits.EMBED_BODY_MAX, description="Body of the embed")
    url: Optional[str] = Field(None, description="URL of the embed")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the embed, in ISO 8601 format")

################################################################################
class EmbedImagesUpdateSchema(BaseSchema):
    """
    Schema for updating images associated with an embed.
    """

    thumbnail_url: Optional[str] = Field(None, description="URL of the thumbnail image for the embed")
    main_image_url: Optional[str] = Field(None, description="URL of the main image for the embed")

################################################################################
class EmbedHeaderUpdateSchema(BaseSchema):
    """
    Schema for updating the header of an embed.
    """

    text: Optional[str] = Field(None, description="Text for the header of the embed")
    icon_url: Optional[str] = Field(None, description="URL of the icon for the header of the embed")
    url: Optional[str] = Field(None, description="URL that the header links to, if applicable")

################################################################################
class EmbedFooterUpdateSchema(BaseSchema):
    """
    Schema for updating the footer of an embed.
    """

    text: Optional[str] = Field(None, description="Text for the footer of the embed")
    icon_url: Optional[str] = Field(None, description="URL of the icon for the footer of the embed")

################################################################################
class EmbedFieldUpdateSchema(BaseSchema):
    """
    Schema for updating a field in an embed.
    Allows partial updates to the field's properties.
    """

    name: Optional[str] = Field(None, max_length=limits.EMBED_FIELD_NAME_MAX, description="Name of the field in the embed")
    value: Optional[str] = Field(None, max_length=limits.EMBED_FIELD_VALUE_MAX, description="Value of the field in the embed")
    inline: Optional[bool] = Field(None, description="Whether the field should be displayed inline with other fields")
    sort_order: Optional[int] = Field(None, description="Sort order of the field in the embed, used for ordering purposes")

################################################################################
