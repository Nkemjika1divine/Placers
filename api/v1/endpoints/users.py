#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized
from models.user import User
from utils.utility import sort_dict_by_values, check_if_word_exists, validate_email_pattern


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
    all_users = []
    for value in users.values():
        all_users.append(value.to_safe_dict())
    return JSONResponse(content=all_users, status_code=status.HTTP_200_OK)


@user_router.get("/users/{user_id}")
def get_a_user(request: Request, user_id: str = None) -> str:
    """GET request for a particular user"""
    from models import storage
    print("In GET userid")
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if not user_id:
        raise Not_Found()
    if user_id == 'me':
        if not request.state.current_user:
            raise Unauthorized("You need to log in first")
        return JSONResponse(content=request.state.current_user.to_safe_dict(), status_code=status.HTTP_200_OK)
    data = storage.all("User")
    for value in data.values():
        if value.id == user_id:
            return JSONResponse(content=value.to_safe_dict(), status_code=status.HTTP_200_OK)
    raise Not_Found("ID is not found")


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
    if request.state.current_user.role != 'superuser':
        raise Unauthorized("You are not allowed to perform this operation")
    data = storage.all("User")
    if not data:
        raise Not_Found()
    for key, value in data.items():
        if value.id == user_id:
            storage.delete(value)
            storage.save()
            return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.get("/users/search/{keyword}")
def search_for_a_user(request: Request, keyword: str = None) -> str:
    """GET method that searches for a user based on the keyword provided"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not keyword:
        raise Not_Found("No keyword entered")
    if not request.state.current_user:
        raise Unauthorized()
    user_list = []
    data = storage.all("User")
    for value in data.values():
        if check_if_word_exists(keyword, value.name):
            user_list.append(value.to_dict())
        elif check_if_word_exists(keyword, value.username):
            user_list.append(value.to_dict())
        return JSONResponse(content=user_list, status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.post("/users")
async def create_a_user(request: Request) -> str:
    from models import storage
    """POST method for creating a new user"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role != 'superuser':
        raise Unauthorized("This is reserved for the superuser only")
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request()
    name = request_body.get("name", None)
    if type(name) is not str:
        raise Bad_Request("Name must be a string")
    username = request_body.get("username", None)
    if not username or type(username) is not str:
        raise Bad_Request("Username missing or not a string")
    if storage.search_key_value("User", "username", username):
        raise Unauthorized("Username taken")
    current_city = request_body.get("current_city", None)
    if type(current_city) is not str:
        raise Bad_Request("current_city must be a string")
    current_country = request_body.get("current_country", None)
    if type(current_country) is not str:
        raise Bad_Request("current_country must be a string")
    email = request_body.get("email", None)
    if not email or type(email) is not str:
        raise Bad_Request("Email missing or not a string")
    if not validate_email_pattern(email):
        raise Unauthorized("Enter a valid email")
    if storage.search_key_value("User", "email", email):
        raise Unauthorized("Email already registered")
    password = request_body.get("password", None)
    if not password or type(password) is not str:
        raise Bad_Request(detail="Password missing or not a string")
    
    new_user = User()
    new_user.name = name
    new_user.username = username
    new_user.current_city = current_city
    new_user.current_country = current_country
    new_user.email = email
    new_user.password = password

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
    if request.state.current_user.role != 'superuser':
        raise Unauthorized("This is reserved for the superuser only")
    all_users = storage.all("User")
    if not all_users:
        return Not_Found()
    user_data = await request.json()
    if not user_data:
        raise Bad_Request()
    for user in all_users.values():
        if user.id == user_id:
            if "name" in user_data:
                if type(user_data['name']) is not str:
                    raise Bad_Request("Name must be a string")
                user.name = user_data["name"]
            if "username" in user_data:
                if type(user_data['username']) is not str:
                    raise Bad_Request("username must be a string")
                if storage.search_key_value("User", "username", user_data["username"]):
                    raise Unauthorized("Username already taken")
                user.username = user_data["username"]
            if 'current_city' in user_data:
                if type(user_data['current_city']) is not str:
                    raise Bad_Request("current_city must be a string")
                user.current_city = user_data['current_city']
            if 'current_country' in user_data:
                if type(user_data['current_country']) is not str:
                    raise Bad_Request("current_country must be a string")
                user.current_country = user_data['current_country']
            if "email" in user_data:
                raise Unauthorized("You are not allowed to change a user's email")
            if "password" in user_data:
                raise Unauthorized("You are not allowed to change a user's password")
            
            user.save()
            return JSONResponse(content=user.to_safe_dict(), status_code=status.HTTP_200_OK)
    raise Not_Found()


@user_router.put("/users/promote/{user_id}")
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
    return JSONResponse(content={"Message": "{} promoted to admin successfully".format(user.display_name())}, status_code=status.HTTP_200_OK)


@user_router.put("/users/demote/{user_id}")
def demote_an_admin(request: Request, user_id: str = None) -> str:
    """PUT method that demotes an admin to a regular user"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not user_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    current_user = request.state.current_user
    if current_user.role != "superuser":
        raise Unauthorized("You are not authorized to perform this operation")
    user = storage.search_key_value("User", "id", user_id)
    if not user:
        raise Not_Found("User does not exist")
    user = user[0]
    user.role = "user"
    user.save()
    return JSONResponse(content={"Message": "{} demoted to user successfully".format(user.display_name())}, status_code=status.HTTP_200_OK)


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
        return JSONResponse(content="This user is yet to record a visit", status_code=status.HTTP_404_NOT_FOUND)
    visit_list = []
    for visit in visits:
        place_id = visit.place_id
        place = storage.search_key_value("Place", "id", place_id)
        visit_list.append(place[0].to_dict())
    return JSONResponse(content=visit_list, status_code=status.HTTP_200_OK)


@user_router.get("/users/place_ranking/{user_id}")
def get_user_place_ranking(request: Request, user_id: str = None) -> str:
    #"""GET method to rank user's ratings of places"""
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
        visit_list[visit.id] = visit.rating
    sorted_visit_list = sort_dict_by_values(visit_list)
    sorted_places = []
    for place in sorted_visit_list:
        sorted_places.append(storage.search_key_value())


@user_router.get("/users/profile")
def user_profile(request: Request) -> str:
    """GET method that Returns the profile of the user"""
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    return JSONResponse(content=request.state.current_user.to_safe_dict(), status_code=status.HTTP_200_OK)


@user_router.put('/profile/update')
async def profile_update(request: Request) -> str:
    """PUT method that Updates the user's profile"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    user = request.state.current_user
    try:
        user_data = await request.json()
    except Exception:
        raise Bad_Request()
    if "name" in user_data:
        if type(user_data['name']) is not str:
            raise Bad_Request("Name must be a string")
        user.name = user_data["name"]
    if "username" in user_data:
        if type(user_data['username']) is not str:
            raise Bad_Request("username must be a string")
        if storage.search_key_value("User", "username", user_data["username"]):
            raise Unauthorized("Username already taken")
        user.username = user_data["username"]
    if 'current_city' in user_data:
        if type(user_data['current_city']) is not str:
            raise Bad_Request("current_city must be a string")
        user.current_city = user_data['current_city']
    if 'current_country' in user_data:
        if type(user_data['current_country']) is not str:
            raise Bad_Request("current_country must be a string")
        user.current_country = user_data['current_country']
    user.save()
    return JSONResponse(content="User successfully updated", status_code=status.HTTP_200_OK)


@user_router.get("/users/best_places_nearby")
def get_best_places_nearby(request: Request) -> str:
    """GET method that returns the best places near a user using average rating"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    all_places = storage.all("Place")
    if not all_places:
        raise Not_Found("no place in the database yet")
    place_list = []
    for place in all_places.values():
        if place.get_average_rating() >= 7:
            place_list.append(place)
    return JSONResponse(content=place_list, status_code=status.HTTP_200_OK)