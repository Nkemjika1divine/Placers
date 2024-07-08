#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request
from models.user import User
from models import storage


user_router = APIRouter()


@user_router.get("/users")
def get_users():
    """GET /api/v1/users
      - Returns all the users in the database"""
    users = storage.all("User")
    if not users:
        raise Not_Found()
    all_users = {}
    for key, value in users:
        all_users[key] = value.to_dict()
    return JSONResponse(content=all_users, status_code=status.HTTP_200_OK)


@user_router.get("/users/{user_id}")
def get_a_user(request: Request, user_id: str = None) -> str:
    """GET request for a particular user"""
    """if not user_id:
        raise Not_Found()"""
    print("checking user")
    if user_id == 'me':
        print("checking current user")
        if not request.state.current_user:
            raise Not_Found()
        return JSONResponse(content=request.state.current_user.to_dict(), status_code=status.HTTP_200_OK)
    print("not me")
    data = storage.all("User")
    for key, value in data:
        if value.id == user_id:
            return JSONResponse(content=value.to_json(), status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.delete("/users/{user_id}")
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
            return JSONResponse(content={}, status_code=status.HTTP_200_OK),
    raise Not_Found()


@user_router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_a_user(request: Request) -> str:
    """POST method for creating a new user"""
    request_body = await request.json()
    if not request_body:
        raise Bad_Request()
    name = request_body.get("name", None)
    username = request_body.get("username", None)
    if not username:
        raise Bad_Request(detail={"error": "Username missing"})
    email = request_body.get("email", None)
    if not email:
        raise Bad_Request(detail={"error": "Email missing"})
    password = request_body.get("hashed_password", None)
    if not password:
        raise Bad_Request(detail={"error": "Password missing"})
    
    new_user = User()
    new_user.name = name
    new_user.username = username
    new_user.email = email
    new_user._hashed_password = password

    new_user.save()
    return JSONResponse(content=new_user.to_dict(), status_code=status.HTTP_201_CREATED)


@user_router.put("/users/{user_id}")
async def edit_user_info(request: Request, user_id: str = None) -> str:
    """PUT method for editing user info"""
    if not user_id:
        raise Not_Found()
    all_users = storage.all("User")
    if not all_users:
        return Not_Found()
    user_data = await request.json()
    if not user_data:
        raise Bad_Request()
    for user in all_users.values():
        if user.id == user_id:
            if "name" in user_data:
                user.name = user_data["name"]
            if "username" in user_data:
                user.name = user_data["username"]
            if "email" in user_data:
                user.name = user_data["email"]
            if "_hashed_password" in user_data:
                user.name = user_data["_hashed_password"]
            
            user.save()
            return JSONResponse(content=user.to_dict(), status_code=status.HTTP_200_OK)
    raise Not_Found()