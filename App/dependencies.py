from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Depends, Path, HTTPException, Header
from sqlalchemy.orm import Session

from .Models import GuildIDModel
from .auth import get_current_user
from .database import get_db
################################################################################
def get_dependencies(
    db: Session = Depends(get_db),
    guild_id: int = Path(..., description="ID of the guild being accessed"),
    x_actor_id: int = Header(..., convert_underscores=False, alias="X-Actor-Id"),
    _: int = Depends(get_current_user),
) -> Dependencies:

    guild_model = db.query(GuildIDModel).filter(GuildIDModel.guild_id == guild_id).first()
    if guild_model is None:
        raise HTTPException(status_code=404, detail="Guild not found")

    return Dependencies(
        db=db,
        guild_id=guild_id,
        actor_id=x_actor_id
    )

################################################################################
@dataclass
class Dependencies:

    db: Session
    guild_id: int
    actor_id: int

################################################################################

