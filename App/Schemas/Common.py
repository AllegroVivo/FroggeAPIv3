from typing import Any, Dict

from pydantic import BaseModel, Field
################################################################################

__all__ = (
    "BaseSchema",
    "IdentifiableSchema",
    "GuildIDSchema",
)

################################################################################
class BaseSchema(BaseModel):
    """
    Base schema for all other schemas in the application.
    It provides a common configuration and validation rules.
    """

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }

################################################################################
class IdentifiableSchema(BaseSchema):
    """
    Schema that includes an identifier field.
    This is typically used for objects that have a unique ID.
    """

    id: int = Field(
        ...,
        description="Unique identifier for the object.",
        ge=1,
    )

################################################################################
class GuildIDSchema(BaseSchema):
    """
    Schema that includes a guild ID field.
    This is used for objects that are associated with a specific guild.
    """

    guild_id: int = Field(
        ...,
        description="Unique identifier for the guild.",
        ge=1,
    )

################################################################################
