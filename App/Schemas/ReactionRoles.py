from __future__ import annotations

from typing import Optional, Any, Dict, List
from pydantic import Field

from .Common import *
################################################################################

__all__ = (
    "ShallowReactionRoleManagerShema",
    "DeepReactionRoleManagerSchema",
    "ShallowReactionRoleMessageSchema",
    "DeepReactionRoleMessageSchema",
    "ReactionRoleSchema",
    "ReactionRoleManagerUpdateSchema",
    "ReactionRoleMessageUpdateSchema",
    "ReactionRoleUpdateSchema",
)

################################################################################
class ShallowReactionRoleManagerShema(BaseSchema):
    """
    Schema for shallow reaction role manager.
    """

    channel_id: Optional[int] = Field(
        ...,
        description="ID of the channel where reaction roles are posted."
    )

################################################################################
class DeepReactionRoleManagerSchema(ShallowReactionRoleManagerShema):
    """
    Full Schema for reaction role manager. Includes all reaction role messages.
    """

    messages: List[DeepReactionRoleMessageSchema] = Field(
        ...,
        description="List of reaction roles messages managed by the app."
    )

################################################################################
class ShallowReactionRoleMessageSchema(IdentifiableSchema):
    """
    Schema representing base data on a reaction role message.
    """

    title: Optional[str] = Field(
        ...,
        description="Title of the message containing the reaction roles."
    )
    description: Optional[str] = Field(
        ...,
        description="Description of the message containing the reaction roles."
    )
    thumbnail_url: Optional[str] = Field(
        ...,
        description="URL of the thumbnail image for the message."
    )
    post_url: Optional[str] = Field(
        ...,
        description="URL of the message in the channel."
    )
    msg_type: int = Field(
        ...,
        description="Type of the reaction message."
    )
    type_param: Optional[int] = Field(
        ...,
        description="Type parameter for the reaction message, if applicable."
    )
    color: Optional[int] = Field(
        ...,
        description="Accent color of the reaction message, if applicable."
    )

################################################################################
class DeepReactionRoleMessageSchema(ShallowReactionRoleMessageSchema):
    """
    Full Schema for reaction role message. Includes all reaction roles.
    """

    roles: List[ReactionRoleSchema] = Field(
        ...,
        description="List of reaction roles in the message."
    )

################################################################################
class ReactionRoleSchema(IdentifiableSchema):
    """
    Schema representing a reaction role.
    """

    label: Optional[str] = Field(
        ...,
        description="Label for the reaction role, if applicable."
    )
    role_id: Optional[int] = Field(
        ...,
        description="ID of the role assigned when the reaction is added."
    )
    emoji: Optional[str] = Field(
        ...,
        description="Emoji used for the reaction role button."
    )

################################################################################
class ReactionRoleManagerUpdateSchema(BaseSchema):
    """
    Schema for updating reaction role manager.
    """

    channel_id: Optional[int] = Field(
        None,
        description="ID of the channel where reaction roles are posted."
    )

################################################################################
class ReactionRoleMessageUpdateSchema(BaseSchema):
    """
    Schema for updating reaction role message.
    """

    title: Optional[str] = Field(
        None,
        description="Title of the message containing the reaction roles."
    )
    description: Optional[str] = Field(
        None,
        description="Description of the message containing the reaction roles."
    )
    thumbnail_url: Optional[str] = Field(
        None,
        description="URL of the thumbnail image for the message."
    )
    post_url: Optional[str] = Field(
        None,
        description="URL of the message in the channel."
    )
    msg_type: Optional[int] = Field(
        None,
        description="Type of the reaction message."
    )
    type_param: Optional[int] = Field(
        None,
        description="Type parameter for the reaction message, if applicable."
    )
    color: Optional[int] = Field(
        None,
        description="Accent color of the reaction message, if applicable."
    )

################################################################################
class ReactionRoleUpdateSchema(BaseSchema):
    """
    Schema for updating a reaction role.
    """

    label: Optional[str] = Field(
        None,
        description="Label for the reaction role, if applicable."
    )
    role_id: Optional[int] = Field(
        None,
        description="ID of the role assigned when the reaction is added."
    )
    emoji: Optional[str] = Field(
        None,
        description="Emoji used for the reaction role button."
    )

################################################################################
