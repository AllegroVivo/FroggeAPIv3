from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

from .Common import *
################################################################################

__all__ = (
    "ReactionRoleManagerModel",
    "ReactionRoleMessageModel",
    "ReactionRoleModel",
)

################################################################################
class ReactionRoleManagerModel(BaseModel):

    __tablename__ = 'reaction_role_managers'

    guild_id = Column(BigInteger, ForeignKey("guild_ids.guild_id", name="reaction_role_managers_guild_ids_fkey"), primary_key=True)
    channel_id = Column(BigInteger, nullable=True)

    # Relationships
    guild = relationship("GuildIDModel", back_populates="role_mgr")
    messages = relationship("ReactionRoleMessageModel", back_populates="manager", uselist=True)

################################################################################
class ReactionRoleMessageModel(BaseModel):

    __tablename__ = 'reaction_role_messages'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("reaction_role_managers.guild_id", name="reaction_role_messages_reaction_role_managers_fkey"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    post_url = Column(String, nullable=True)
    msg_type = Column(Integer, nullable=False, default=1, server_default="1")
    type_param = Column(Integer, nullable=True)
    color = Column(Integer, nullable=True)

    # Relationships
    manager = relationship("ReactionRoleManagerModel", back_populates="messages", uselist=False)
    roles = relationship("ReactionRoleModel", back_populates="parent", uselist=True)

################################################################################
class ReactionRoleModel(BaseModel):

    __tablename__ = 'reaction_roles'

    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger, ForeignKey("reaction_role_messages.id", name="reaction_roles_reaction_role_messages_fkey"), nullable=False)
    role_id = Column(BigInteger, nullable=True)
    emoji = Column(String, nullable=True)
    label = Column(String, nullable=True)

    # Relationships
    parent = relationship("ReactionRoleMessageModel", back_populates="roles", uselist=False)

################################################################################
