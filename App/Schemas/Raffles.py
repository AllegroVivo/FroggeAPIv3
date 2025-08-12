from __future__ import annotations

from datetime import datetime
from typing import Optional, Any, Dict, List
from pydantic import Field, field_validator

from .Common import *
################################################################################

__all__ = (
    "ShallowRaffleManagerSchema",
    "DeepRaffleManagerSchema",
    "ShallowRaffleSchema",
    "DeepRaffleSchema",
    "RaffleEntrySchema",
    "RaffleManagerUpdateSchema",
    "RaffleUpdateSchema",
    "RaffleEntryUpdateSchema",
    "RaffleEntryCreateSchema",
)

################################################################################
class ShallowRaffleManagerSchema(BaseSchema):
    """
    Schema for a shallow representation of a raffle manager.
    """

    channel_id: Optional[int] = Field(..., description="The channel ID where raffles are posted.")

################################################################################
class DeepRaffleManagerSchema(ShallowRaffleManagerSchema):
    """
    Schema for a deep representation of a raffle manager, including its fully hydrated raffles.
    """

    raffles: List[DeepRaffleSchema] = Field(
        ...,
        description="A list of raffles managed by this raffle manager.",
    )

################################################################################
class ShallowRaffleSchema(IdentifiableSchema):
    """
    Schema for a shallow representation of a raffle.
    """

    winners: List[int] = Field(..., description="The winners of the raffle.")
    is_active: bool = Field(..., description="Whether this raffle is the current active raffle.")
    post_url: Optional[str] = Field(..., description="The URL of the post related to the raffle.")
    name: Optional[str] = Field(..., description="The name of the raffle.")
    prize: Optional[str] = Field(..., description="The prize for the raffle.")
    num_winners: Optional[int] = Field(..., description="The number of winners for the raffle.")
    auto_notify: bool = Field(..., description="Whether to automatically notify winners.")
    cost: int = Field(..., description="The cost of a single ticket in the raffle.")
    rolled_at: Optional[datetime] = Field(..., description="The time when the raffle was rolled.")
    rolled_by: Optional[int] = Field(..., description="The user who rolled the raffle.")

    # This validator is present because there were some weird bugs when loading
    # the winners field from the database. It always comes in as a string
    # representation of a list, despite the column's default behavior matching
    # all other list fields in the application, so we need to handle that case.
    # Note: The `field_validator` decorator must come FIRST.
    # noinspection PyNestedDecorators
    @field_validator('winners', mode='before')
    @classmethod
    def parse_winners(cls, v):
        if isinstance(v, str):
            import json
            return json.loads(v) if v else []
        return v or []

################################################################################
class DeepRaffleSchema(ShallowRaffleSchema):
    """
    Schema for a deep representation of a raffle, including its details and entries.
    """

    entries: List[RaffleEntrySchema] = Field(..., description="A list of entries in the raffle.")

################################################################################
class RaffleEntrySchema(IdentifiableSchema):
    """
    Schema for an entry in a raffle.
    """

    user_id: int = Field(..., description="The user ID of the person who entered the raffle.")
    quantity: int = Field(..., description="The number of tickets purchased by the user for this raffle.")

################################################################################
class RaffleManagerUpdateSchema(BaseSchema):
    """
    Schema for updating a raffle manager.
    """

    channel_id: Optional[int] = Field(None, description="The channel ID where raffles are posted.")

################################################################################
class RaffleUpdateSchema(BaseSchema):
    """
    Schema for updating a raffle.
    """

    winners: List[int] = Field(None, description="The winners of the raffle.")
    is_active: bool = Field(None, description="Whether this raffle is the current active raffle.")
    post_url: Optional[str] = Field(None, description="The URL of the post related to the raffle.")
    name: Optional[str] = Field(None, description="The name of the raffle.")
    prize: Optional[str] = Field(None, description="The prize for the raffle.")
    num_winners: Optional[int] = Field(None, description="The number of winners for the raffle.")
    auto_notify: bool = Field(None, description="Whether to automatically notify winners.")
    cost: int = Field(None, description="The cost of a single ticket in the raffle.")
    rolled_at: Optional[datetime] = Field(None, description="The time when the raffle was rolled.")
    rolled_by: Optional[int] = Field(None, description="The user who rolled the raffle.")

################################################################################
class RaffleEntryUpdateSchema(BaseSchema):
    """
    Schema for updating a raffle entry.
    """

    quantity: int = Field(None, description="The number of tickets purchased by the user for this raffle.")

################################################################################
class RaffleEntryCreateSchema(BaseSchema):

    user_id: int = Field(..., description="The user ID of the person who entered the raffle.")
    quantity: int = Field(..., description="The number of tickets purchased by the user for this raffle.")

################################################################################
