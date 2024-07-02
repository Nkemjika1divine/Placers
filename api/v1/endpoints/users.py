#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Unauthorized, Forbidden
from models.user import User
from models import storage


user_router = APIRouter()


user_router.get("/users")
def get_users():
    """GET /api/v1/users
      - Returns all the users in the database"""
    users = storage.all("User")
    return JSONResponse(users)