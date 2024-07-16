#!/usr/bin/python3
"""Module for session authentication endpoints"""
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, Request, status
from api.v1.error_handlers import *
from os import environ
from utils.utility import validate_email_pattern


load_dotenv()


session_router = APIRouter()


@session_router.post("/session/create_account")
async def create_account(request: Request):
    """Handles account creation"""
    from models.user import User
    from models import storage
    if not request:
        raise Bad_Request()
    try:
        request_body = await request.json()
    except Exception as error:
        raise Bad_Request(error)
    
    if not storage.all("User"):
        role = 'superuser'
    else:
        role = 'user'

    name = request_body.get("name", None)
    if type(name) is not str:
        raise Bad_Request("name must be a string")
    username = request_body.get("username")
    if not username or type(username) is not str:
        raise Bad_Request("Username missing or not a string")
    existing_user = storage.search_key_value("User", "username", username)
    if existing_user:
        raise Forbidden("Username taken")
    
    email = request_body.get("email", None)
    if not email or type(email) is not str:
        raise Bad_Request("Email missing or not a string")
    if not validate_email_pattern(email):
        raise Forbidden("Wrong email format")
    existing_user = storage.search_key_value("User", "email", email)
    if existing_user:
        raise Forbidden("Email already registered")
    
    password = request_body.get("password", None)
    if not password or type(password) is not str:
        raise Bad_Request("Password missing or not a string")
    
    user = User(name=name, username=username, email=email, password=password, role=role)
    storage.new(user)
    storage.save()
    return JSONResponse(content=user.to_safe_dict(), status_code=status.HTTP_201_CREATED)
    



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
    # set cookie with an expiry date
    expiry_date = datetime.now(timezone.utc) + timedelta(days=30)
    response.set_cookie(key=environ.get("SESSION_NAME"), value=session_id, expires=expiry_date)
    return response


@session_router.delete("/session/logout")
def logout(request: Request):
    """Logs out a user by deleting the user's session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        raise Not_Found("User not found")
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)

@session_router.get("/session/send_verification_token")
def send_token_for_email(request: Request) -> str:
    """GET method for sending verification tokens"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.send_email_token():
        return JSONResponse(content="Email verification token sent", status_code=status.HTTP_200_OK)
    raise Unauthorized()


@session_router.post("/session/verify_token")
async def verify_email_token(request: Request) -> str:
    """Checks if the verification token is the same as the one stored"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request()
    if 'reset_token' not in request_body:
        raise Not_Found("token required")
    user = request.state.current_user
    if user.reset_token == request_body["reset_token"]:
        user.reset_token = None
        user.email_verified = "yes"
        user.save()
        return JSONResponse(content="Email validated", status_code=status.HTTP_200_OK)
    raise Unauthorized()