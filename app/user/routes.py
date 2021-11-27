import os
from datetime import timedelta
from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, Security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from user.service import UserService
from utils.security import Token, create_access_token, get_current_user, Role, roles_allowed
from user.models import User, UserBase, UserCreate

users = APIRouter(prefix='/users', tags=["Users"])

#-----------------------------------------------------------------------------
# CRUD
#-----------------------------------------------------------------------------
@users.get(
    path="",
    description="Get All Users",
    response_model=List[User],
    responses={
        200: { "description": "Users are returned" },
        400: { "description": "Error" }
    },
    dependencies=[Security(roles_allowed, scopes=[Role.admin])]
)
async def get_all() -> JSONResponse:
    return await UserService().get_all()

@users.get(
    path="/{id}",
    description="Get User By Id",
    response_model=User,
    responses={
        200: { "description": "User is returned" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    },
    dependencies=[Security(roles_allowed, scopes=[Role.admin])]
)
async def get(id: UUID) -> JSONResponse:
    user = await UserService().get(id)
    if user is not None:
        return user
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User with id {" + str(id) + " } not found!")

@users.post(
    path="",
    description="Create User",
    status_code=201,
    response_model=User,
    responses={
        201: { "description": "User is created" },
        400: { "description": "Could not insert User" }
    }
)
async def create(create: UserCreate) -> JSONResponse:
    registerd_user = await UserService().create(create)
    if registerd_user is not None:
        return registerd_user
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Could not register User")

@users.delete(
    path="",
    description="Delete User",
    status_code=204,
    response_model=None,
    responses={
        204: { "description": "User was deleted" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    },
    dependencies=[Security(roles_allowed, scopes=[Role.admin])]
)
async def delete(id: UUID) -> Response:
    if await UserService().delete(id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Could not delete User")

@users.put(
    path="/{id}",
    description="Update User",
    status_code=204,
    response_model=None,
    responses={
        204: { "description": "User was updated" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    },
    dependencies=[Security(roles_allowed, scopes=[Role.admin])]
)
async def update(id: UUID, update: UserBase):
    if  await UserService().update(id, update):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Could not update User")

#-----------------------------------------------------------------------------
# CRUD Extensions
#-----------------------------------------------------------------------------

@users.get(
    path="/by-username/{username}",
    description="Get User By Name",
    response_model=User,
    responses={
        200: { "description": "User is returned" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    },
    dependencies=[Security(roles_allowed, scopes=[Role.admin])]
)
async def get_by_name(username: str) -> JSONResponse:
    user = await UserService().get_by_name(username)
    if user is not None:
        return user
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="User with id {" + id + " } not found!")

#-----------------------------------------------------------------------------
# Preferred User
#-----------------------------------------------------------------------------
@users.get(
    path="/get/me",
    description="Get Preferred User",
    response_model=User,
    responses={
        200: { "description": "User is returned" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    }
)
async def get_me(userid: UUID = Depends(get_current_user)):
    return await get(userid)

@users.put(
    path="/update/me",
    description="Update Preferred User",
    status_code=204,
    response_model=None,
    responses={
        204: { "description": "User was updated" },
        304: { "description": "User not modified" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    }
)
async def update_me(update_request: UserBase, userid: UUID = Depends(get_current_user)):
    return await update(userid, update_request)
        
@users.patch(
    path="/password/{password}",
    description="Change Password",
    status_code=204,
    response_model=None,
    responses={
        204: { "description": "User was updated" },
        400: { "description": "Error" },
        404: { "description": "User not found" }
    }
)
async def patch_password(password: str, userid: UUID = Depends(get_current_user)):
    if await UserService().patch_password(userid, password):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Could not update password")

#-----------------------------------------------------------------------------
# Authentication
#-----------------------------------------------------------------------------
@users.post(
    path="/auth",
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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            Token(
                access_token=access_token, 
                token_type="bearer"
            )
        )
    )

@users.post(
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