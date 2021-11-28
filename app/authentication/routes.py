
import os
from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from user.service import UserService
from utils.security import Token, create_access_token, get_current_user


auth = APIRouter(prefix='/auth', tags=["Athentication"])

#-----------------------------------------------------------------------------
# Authentication
#-----------------------------------------------------------------------------
@auth.post(
    path="",
    description="Authenticate User",
    response_model=Token,
    responses={
        200: { "description": "Valid User credentials" },
        400: { "description": "Error" },
        401: { "description": "Invalid User credentials" }
    }
)
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserService().authenticate_user(form_data.username, form_data.password)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = await create_access_token(
        data = {"sub": str(user.id), "active": user.active, "roles": user.roles }, 
        expires_delta = access_token_expires
    )
    return Token(access_token = access_token, token_type = "bearer")

@auth.post(
    path="/token",
    description="Refresh Token",
    response_model=Token,
    responses={
        200: { "description": "Token refreshed" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    }
)
async def token(userid: UUID = Depends(get_current_user)):
    user = await UserService().get(userid)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found")
    access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = await create_access_token(
        data = {"sub": str(user.id), "active": user.active, "roles": user.roles }, 
        expires_delta = access_token_expires
    )
    return Token(access_token = access_token, token_type = "bearer")

@auth.post(
    path="/logout",
    description="Logout",
    status_code=204,
    response_model=None,
    responses={
        204: { "description": "User logged out" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    }
)
async def logout(userid: UUID = Depends(get_current_user)):
    await UserService().clear_from_cache(userid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)