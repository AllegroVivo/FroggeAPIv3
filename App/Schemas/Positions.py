from __future__ import annotations

from typing import Optional, Any, Dict
from pydantic import Field

from .Common import *
################################################################################

__all__ = ("PositionSchema", "PositionUpdateSchema")

################################################################################
# READ Schemas
################################################################################
class PositionSchema(IdentifiableSchema):

    name: Optional[str] = Field(..., description="The name of the position.")
    role_id: Optional[int] = Field(..., description="The role ID associated with the position.")

################################################################################
class PositionUpdateSchema(BaseSchema):

    name: Optional[str] = Field(None, description="The name of the position.")
    role_id: Optional[int] = Field(None, description="The role ID associated with the position.")

################################################################################
