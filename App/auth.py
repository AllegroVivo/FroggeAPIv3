from datetime import datetime, timedelta, UTC
from typing import Dict, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from . import Schemas
################################################################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

################################################################################
def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """

    return pwd_context.hash(password)

################################################################################
def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.
    """

    return pwd_context.verify(password, hashed_password)

################################################################################
def generate_access_token(data: Dict[str, Any]) -> str:
    """
    Generate a JWT access token.
    """

    to_encode = data.copy()

    expires_delta = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_delta})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

################################################################################
def verify_access_token(token: str) -> Schemas.TokenDataSchema:
    """
    Verify the access token and return the token data.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID not found", headers={"WWW-Authenticate": "Bearer"})
        return Schemas.TokenDataSchema(id=int(user_id))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Password", headers={"WWW-Authenticate": "Bearer"})

################################################################################
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the access token.
    """

    return verify_access_token(token)

################################################################################
