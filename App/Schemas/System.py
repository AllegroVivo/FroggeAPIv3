from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from pydantic import Field
from App import limits

from .Common import *
################################################################################

__all__ = (
    "RegistrationSchema",
    "RegistrationResponseSchema",
    "LoginResponseSchema",
    "LoginSchema",
    "AccessTokenSchema",
    "TokenDataSchema",
)

################################################################################
class RegistrationSchema(BaseSchema):

    user_id: int
    password: str
    frogge: str

################################################################################
class RegistrationResponseSchema(BaseSchema):

    user_id: int
    created_at: datetime
    last_login: Optional[datetime]

################################################################################
class LoginResponseSchema(BaseSchema):

    access_token: str
    token_type: str = Field(default="bearer")

################################################################################
class LoginSchema(BaseSchema):

    user_id: int
    password: str

################################################################################
class AccessTokenSchema(LoginResponseSchema):

    actor_id: int

################################################################################
class TokenDataSchema(BaseSchema):

    id: Optional[int] = None

################################################################################
