from __future__ import annotations

from typing import Optional, Any, Dict
from pydantic import Field

from .Common import *
################################################################################

__all__ = ("GlyphMessageSchema", "GlyphMessageUpdateSchema")

################################################################################
# READ Schemas
################################################################################
class GlyphMessageSchema(IdentifiableSchema):

    name: Optional[str] = Field(..., description="The name of the glyph message.")
    message: Optional[str] = Field(..., description="The content of the glyph message.")

################################################################################
class GlyphMessageUpdateSchema(BaseSchema):

    name: Optional[str] = Field(None, description="The name of the glyph message.")
    message: Optional[str] = Field(None, description="The content of the glyph message.")

################################################################################
