#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized
from models.user import User


user_router = APIRouter()


@user_router.get("/users")
def get_users(request: Request):
    """GET /api/v1/users
      - Returns all the users in the database"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    users = storage.all("User")
    if not users:
        raise Not_Found()
    all_users = {}
    for key, value in users:
        all_users[key] = value.to_safe_dict()
    return JSONResponse(content=all_users, status_code=status.HTTP_200_OK)


@user_router.get("/users/{user_id}")
def get_a_user(request: Request, user_id: str = None) -> str:
    """GET request for a particular user"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if not user_id:
        raise Not_Found()
    if user_id == 'me':
        if not request.state.current_user:
            raise Not_Found()
        return JSONResponse(content=request.state.current_user.to_safe_dict(), status_code=status.HTTP_200_OK)
    data = storage.all("User")
    for key, value in data:
        if value.id == user_id:
            return JSONResponse(content=value.to_safe_dict(), status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.delete("/users/{user_id}")
def delete_user(request: Request, user_id: str = None) -> str:
    """DELETE request: Deletes a user"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if not user_id:
        raise Not_Found()
    data = storage.all("User")
    if not data:
        raise Not_Found()
    for key, value in data.items():
        if value.id == user_id:
            storage.delete(value)
            return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_a_user(request: Request) -> str:
    from models import storage
    """POST method for creating a new user"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request()
    name = request_body.get("name", None)
    username = request_body.get("username", None)
    if not username:
        raise Bad_Request(detail="Username missing")
    if storage.search_key_value("User", "username", username):
        raise Unauthorized("Username taken")
    email = request_body.get("email", None)
    if not email:
        raise Bad_Request(detail="Email missing")
    if storage.search_key_value("User", "email", email):
        raise Unauthorized("Email already registered")
    password = request_body.get("hashed_password", None)
    if not password:
        raise Bad_Request(detail="Password missing")
    
    new_user = User()
    new_user.name = name
    new_user.username = username
    new_user.email = email
    new_user._hashed_password = password

    new_user.save()
    return JSONResponse(content=new_user.to_safe_dict(), status_code=status.HTTP_201_CREATED)


@user_router.put("/users/{user_id}")
async def edit_user_info(request: Request, user_id: str = None) -> str:
    """PUT method for editing user info"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
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
            return JSONResponse(content=user.to_safe_dict(), status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.put("/users/upgrade_role/{user_id}")
def upgrade_user_role(request: Request, user_id: str = None):
    """PUT method for upgrading a user to admin"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    current_user = request.state.current_user
    if current_user.role == "user":
        raise Unauthorized("You are not authorized to perform this operation")
    updater_id = current_user.id
    user = storage.search_key_value("User", "id", user_id)
    if not user:
        raise Not_Found("User does not exist")
    user = user[0]
    user.role = "admin"
    user.role_updater = updater_id
    user.save()
    return JSONResponse(content={"Message": "{} upgraded to admin".format(user.display_name())}, status_code=status.HTTP_200_OK)


@user_router.get("/users/visit_history/{user_id}")
def get_user_visit_history(request: Request, user_id: str = None) -> str:
    """GET method that returns the user's visit history"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    visits = storage.search_key_value("Review", "user_id", user_id)
    if not visits:
        return JSONResponse(content={"message": "This user is yet to record a visit"}, status_code=status.HTTP_404_NOT_FOUND)
    visit_list = []
    for visit in visits:
        place_id = visit.place_id
        place = storage.search_key_value("Place", "id", place_id)
        visit_list.append(place[0].to_dict())
    return JSONResponse(content=visit_list, status_code=status.HTTP_200_OK)


"""@user_router.get("/users/place_ranking/{user_id}")
def get_user_place_ranking(request: Request, user_id: str = None) -> str:
    """"GET method to rank user's ratings of places""""""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    visits = storage.search_key_value("Review", "user_id", user_id)
    if not visits:
        return JSONResponse(content={"message": "This user is yet to record a visit"}, status_code=status.HTTP_404_NOT_FOUND)
    visit_list = {}
    for visit in visits:
        visit_list[visit.id] = visit.rating"""
        