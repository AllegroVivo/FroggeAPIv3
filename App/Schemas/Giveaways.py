from __future__ import annotations
from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import Field
from App import limits

from .Common import *
################################################################################

__all__ = (
    "ShallowGiveawayManagerSchema",
    "DeepGiveawayManagerSchema",
    "ShallowGiveawaySchema",
    "DeepGiveawaySchema",
    "GiveawayDetailsSchema",
    "GiveawayEntrySchema",
    "GiveawayEntryCreateSchema",
    "GiveawayManagerUpdateSchema",
    "GiveawayUpdateSchema",
    "GiveawayDetailsUpdateSchema",
)

################################################################################
class ShallowGiveawayManagerSchema(BaseSchema):
    """
    Schema for a shallow representation of a giveaway manager.
    """

    channel_id: Optional[int] = Field(..., description="The channel ID where giveaways are managed.")

################################################################################
class DeepGiveawayManagerSchema(ShallowGiveawayManagerSchema):
    """
    Schema for a deep representation of a giveaway manager, including its fully hydrated giveaways.
    """

    giveaways: List[DeepGiveawaySchema] = Field(
        ...,
        description="A list of giveaways managed by this giveaway manager.",
    )

################################################################################
class ShallowGiveawaySchema(IdentifiableSchema):
    """
    Schema for a shallow representation of a giveaway.
    """

    winners: List[int] = Field(..., description="The winners of the giveaway.")
    post_url: Optional[str] = Field(..., description="The URL of the post related to the giveaway.")
    rolled_at: Optional[datetime] = Field(..., description="The timestamp when the giveaway was rolled.")
    rolled_by: Optional[int] = Field(..., description="The user ID of the person who rolled the giveaway.")

################################################################################
class DeepGiveawaySchema(ShallowGiveawaySchema):
    """
    Schema for a deep representation of a giveaway, including its details and entries.
    """

    details: GiveawayDetailsSchema = Field(..., description="The details of the giveaway.")
    entries: List[GiveawayEntrySchema] = Field(..., description="A list of entries in the giveaway.")

################################################################################
class GiveawayDetailsSchema(BaseSchema):
    """
    Schema for the details of a giveaway.
    """

    name: Optional[str] = Field(..., description="The name of the giveaway.")
    prize: Optional[str] = Field(..., description="The prize for the giveaway.")
    num_winners: int = Field(..., description="The number of winners for the giveaway.")
    auto_notify: bool = Field(..., description="Whether to automatically notify winners.")
    description: Optional[str] = Field(..., description="A description of the giveaway.")
    thumbnail_url: Optional[str] = Field(..., description="The URL of the thumbnail image for the giveaway.")
    color: Optional[int] = Field(..., description="The color associated with the giveaway.")
    end_dt: Optional[datetime] = Field(..., description="The end date and time of the giveaway.")
    emoji: Optional[str] = Field(..., description="The emoji associated with the giveaway.")

################################################################################
class GiveawayEntrySchema(IdentifiableSchema):
    """
    Schema for an entry in a giveaway.
    """

    user_id: int = Field(..., description="The user ID of the participant in the giveaway.")
    timestamp: datetime = Field(..., description="The timestamp when the entry was made.")

################################################################################
class GiveawayEntryCreateSchema(BaseSchema):
    """
    Schema for creating a new entry in a giveaway.
    """

    user_id: int = Field(..., description="The user ID of the participant in the giveaway.")

################################################################################
class GiveawayManagerUpdateSchema(BaseSchema):
    """
    Schema for updating a giveaway manager.
    """

    channel_id: Optional[int] = Field(None, description="The channel ID where giveaways are managed.")

################################################################################
class GiveawayUpdateSchema(BaseSchema):
    """
    Schema for updating a giveaway.
    """

    winners: Optional[List[int]] = Field(None, description="The winners of the giveaway.")
    post_url: Optional[str] = Field(None, description="The URL of the post related to the giveaway.")
    rolled_at: Optional[datetime] = Field(None, description="The timestamp when the giveaway was rolled.")
    rolled_by: Optional[int] = Field(None, description="The user ID of the person who rolled the giveaway.")

################################################################################
class GiveawayDetailsUpdateSchema(BaseSchema):
    """
    Schema for updating the details of a giveaway.
    """

    name: Optional[str] = Field(None, description="The name of the giveaway.")
    prize: Optional[str] = Field(None, description="The prize for the giveaway.")
    num_winners: Optional[int] = Field(None, description="The number of winners for the giveaway.")
    auto_notify: Optional[bool] = Field(None, description="Whether to automatically notify winners.")
    description: Optional[str] = Field(None, description="A description of the giveaway.")
    thumbnail_url: Optional[str] = Field(None, description="The URL of the thumbnail image for the giveaway.")
    color: Optional[int] = Field(None, description="The color associated with the giveaway.")
    end_dt: Optional[datetime] = Field(None, description="The end date and time of the giveaway.")
    emoji: Optional[str] = Field(None, description="The emoji associated with the giveaway.")

################################################################################

