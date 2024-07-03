#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Unauthorized, Forbidden, Not_Found
from models.user import User
from models import storage


user_router = APIRouter()


@user_router.get("/users")
def get_users():
    """GET /api/v1/users
      - Returns all the users in the database"""
    users = storage.all("User")
    return JSONResponse(content=users, status_code=200)


@user_router.get("/users/<user_id")
def get_a_user(user_id: str = None) -> str:
    """GET request for a particular user"""
    if not user_id:
        raise Not_Found()
    data = storage.all("User")
    for key, value in data:
        if value.id == user_id:
            return JSONResponse(content=value.to_json(), status_code=200)
    raise Not_Found()


@user_router.delete("/users/<user_id>")
def delete_user(user_id: str = None) -> str:
    """DELETE request: Deletes a user"""
    if not user_id:
        raise Not_Found()
    data = storage.all("User")
    if not data:
        raise Not_Found()
    for key, value in data.items():
        if value.id == user_id:
            storage.delete(value)
            return JSONResponse(content={}, status_code=200),
    raise Not_Found()