#!/usr/bin/python3
"""Module for session authentication endpoints"""
from dotenv import load_dotenv
from fastapi import APIRouter, Request, status
from api.v1.error_handlers import *
from os import environ


load_dotenv()


session_router = APIRouter()


@session_router.post("/session/login")
async def login(request: Request) -> str:
    """Handles Login operations"""
    from api.v1.app import auth
    from models import storage
    if not request:
        raise Bad_Request()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    email = request_body.get("email")
    hashed_password = request_body.get("password")
    if not email:
        raise Bad_Request("Email required")
    if not hashed_password:
        raise Bad_Request("Password required")
    # Get the user with the email
    user = storage.search_key_value("User", "email", email)
    if not user:
        raise Not_Found("No user found for this email")
    # Check if the password is valid
    if not user[0].is_valid_password(hashed_password):
        raise Unauthorized("Wrong password")
    # create a session id for the user
    session_id = auth.create_session(user[0].id)
    response = JSONResponse(user[0].to_dict())
    response.set_cookie(key=environ.get("SESSION_NAME"), value=session_id)
    return response

@session_router.delete("/session/logout")
async def logout(request: Request):
    """Logs out a user by deleting the user's session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        raise Not_Found("User not found")
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)