import os
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from uuid import UUID
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from fastapi.security.oauth2 import OAuth2PasswordBearer, SecurityScopes
from pydantic.main import BaseModel

class Role(str, Enum):
    admin = "admin"
    user = "user"

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/users/auth"
)

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(to_encode, os.environ.get("ACCESS_TOKEN_SECRET_KEY"), os.environ.get("ACCESS_TOKEN_ALGORITHM"))
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, os.environ.get("ACCESS_TOKEN_SECRET_KEY"), algorithms=[os.environ.get("ACCESS_TOKEN_ALGORITHM")])
        userid: UUID = UUID(payload.get("sub"))
        active: bool = payload.get("active")
        if userid is None and active:
            raise credentials_exception
        return userid
    except JWTError:
        raise credentials_exception

async def roles_allowed(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, os.environ.get("ACCESS_TOKEN_SECRET_KEY"), algorithms=[os.environ.get("ACCESS_TOKEN_ALGORITHM")])
        roles: List[Role] = payload.get("roles")
        if len(security_scopes.scopes) > 0:
            if not any(role in roles for role in security_scopes.scopes):
                raise credentials_exception
    except JWTError:
        raise credentials_exception
