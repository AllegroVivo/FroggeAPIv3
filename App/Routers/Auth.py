from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import Models, Schemas, auth
from ..dependencies import get_db
from ..config import settings
################################################################################

router = APIRouter(prefix="/auth", tags=["System Authentication"])

################################################################################
@router.post("/register", status_code=201, response_model=Schemas.RegistrationResponseSchema)
def register_user(
    data: Schemas.RegistrationSchema,
    db: Session = Depends(get_db)
) -> Schemas.RegistrationResponseSchema:

    if db.query(Models.UserModel).filter_by(user_id=data.user_id).first():
        raise HTTPException(status_code=400, detail=f"User ID '{data.user_id}' already exists")

    if data.frogge != settings.FROGGE_REGISTRATION_PASSWORD:
        raise HTTPException(
            status_code=403,
            detail=(
                "You are not authorized to register as a user. Speak to Allegro for "
                "more information on becoming registered. ♥"
            )
        )

    new_user = Models.UserModel(user_id=data.user_id, password=auth.hash_password(data.password))
    db.add(new_user)
    db.flush()
    db.refresh(new_user)

    return Schemas.RegistrationResponseSchema.model_validate(new_user)

################################################################################
@router.post("/login", response_model=Schemas.LoginResponseSchema)
def login_user(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Schemas.LoginResponseSchema:

    user = db.query(Models.UserModel).filter_by(user_id=data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    if not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})

    token = auth.generate_access_token(data={"user_id": user.user_id})
    return Schemas.LoginResponseSchema(access_token=token)

################################################################################
