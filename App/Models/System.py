from __future__ import annotations

from sqlalchemy import Column, Integer, String, BigInteger, UUID, TIMESTAMP, func, JSON

from .Common import BaseModel
################################################################################

__all__ = ("AuditLogModel", "UserModel")

################################################################################
class UserModel(BaseModel):

    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    last_login = Column(TIMESTAMP, nullable=True)

################################################################################
class AuditLogModel(BaseModel):

    __tablename__ = 'audit_log'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, nullable=False)
    target = Column(String, nullable=False)
    target_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    changes = Column(JSON, nullable=False)
    request_id = Column(UUID, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

################################################################################
