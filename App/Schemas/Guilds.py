from __future__ import annotations

from pydantic import RootModel, Field
from typing import List, Optional

from .Common import *
from .Embeds import DeepEmbedSchema
################################################################################

__all__ = (
    "FullHydrationSchema",
    "TopLevelGuildSchema",
    "GuildDataSchema",
    "GuildConfigurationSchema",
    "GuildConfigurationUpdateSchema",
)

################################################################################
class FullHydrationSchema(RootModel):
    """
    Schema for full hydration of guild data, including all guilds and their configurations.
    Typically reserved for bot startup or administrative tasks.
    """

    root: List[TopLevelGuildSchema] = Field(
        default_factory=list,
        description="A list of guilds with their full deep data models.",
    )

################################################################################
class TopLevelGuildSchema(BaseSchema):
    """
    Schema for a top-level guild, containing the guild ID and its associated data.
    """

    guild_id: int = Field(..., description="The unique identifier for the guild associated with this data.")
    data: GuildDataSchema = Field(..., description="The full data associated with the guild..")

################################################################################
class GuildDataSchema(BaseSchema):
    """
    Container schema for guild data.
    """

    configuration: GuildConfigurationSchema = Field(..., description="The configuration settings for the guild.")
    embeds: List[DeepEmbedSchema] = Field(
        default_factory=list,
        description="A list of custom embeds associated with the guild.",
    )

################################################################################
class GuildConfigurationSchema(BaseSchema):
    """
    Schema for guild configuration.
    """

    timezone: int = Field(..., description="The timezone for the guild.")
    log_channel_id: Optional[int] = Field(..., description="The ID of the channel where logs are sent.")

################################################################################
class GuildConfigurationUpdateSchema(BaseSchema):
    """
    Schema for updating guild configuration.
    """

    timezone: Optional[int] = Field(None, description="The timezone for the guild.")
    log_channel_id: Optional[int] = Field(None, description="The ID of the channel where logs are sent.")
    # The guild router is directly attached to the main trunk. This means that we
    # bypass the normal behavior of requiring an X-Actor-Id header for updates.
    # Instead, we require an editor_id field in the body of the request.
    editor_id: int = Field(..., description="The ID of the user making the changes to the guild configuration.")

################################################################################
