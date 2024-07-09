#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Unauthorized, Forbidden, Not_Found, Bad_Request
from models.place import Place
from models.user import User
from models import storage
from utils.utility import check_if_word_exists


place_router = APIRouter()


@place_router.get("/places")
def get_places(request: Request) -> str:
    """GET /api/v1/users
      - Returns all the places in the database"""
    if not request:
        return Bad_Request()
    if request.state.current_user:
        places = storage.all("Place")
        if not places:
            raise Not_Found()
        all_places = {}
        for key, value in places:
            all_places[key] = value.to_dict()
        return JSONResponse(content=all_places, status_code=status.HTTP_200_OK)
    raise Unauthorized()


@place_router.get("/places/{place_id}")
def get_a_place(request: Request, place_id: str = None) -> str:
    """GET request for a particular place"""
    if not request:
        return Bad_Request()
    if request.state.current_user:
        if not place_id:
            raise Not_Found()
        data = storage.all("Place")
        for value in data.values():
            if value.id == place_id:
                return JSONResponse(content=value.to_dict(), status_code=status.HTTP_200_OK)
        raise Not_Found()
    raise Unauthorized()


@place_router.get("/places/search/{keyword}")
def search_for_a_place(request: Request, keyword: str = None) -> str:
    """GET request to search for a particular place with a name"""
    if not request:
        return Bad_Request()
    if request.state.current_user:
        if not keyword:
            raise Not_Found()
        place_list = []
        data = storage.all("Place")
        for value in data.values():
            if check_if_word_exists(keyword, value.name):
                place_list.append(value.to_dict())
            elif check_if_word_exists(keyword, value.category):
                place_list.append(value.to_dict())
            elif check_if_word_exists(keyword, value.address):
                place_list.append(value.to_dict())
            elif check_if_word_exists(keyword, value.city):
                place_list.append(value.to_dict())
            elif check_if_word_exists(keyword, value.state):
                place_list.append(value.to_dict())
            elif check_if_word_exists(keyword, value.country):
                place_list.append(value.to_dict())
            return JSONResponse(content=place_list, status_code=status.HTTP_200_OK)
        raise Not_Found()
    raise Unauthorized()


@place_router.delete("/places/{place_id}")
def delete_a_place(request: Request, place_id: str = None,) -> str:
    """DELETE method that a place"""
    if not request:
        return Bad_Request()
    if request.state.current_user:
        if request.state.current_user.role == "user":
            raise Unauthorized()
        if not place_id:
            raise Not_Found()
        data = storage.all("Place")
        if not data:
            raise Not_Found()
        for value in data.values():
            if value.id == place_id:
                storage.delete(value)
                return JSONResponse(content={}, status_code=status.HTTP_200_OK)
        raise Not_Found()
    raise Unauthorized()

@place_router.post("/places")
async def add_place(request: Request):
    """Adds a new place to the database"""
    if not request:
        return Bad_Request()
    if request.state.current_user:
        user_id = request.state.current_user.id
        try:
            request_body = await request.json()
        except Exception:
            raise Bad_Request()
        
        name = request_body.get("name", None)
        if not name:
            raise Bad_Request("There must be a name for the place")
        category = request_body.get("category", None)
        description = request_body.get("description", None)
        if not category:
            raise Bad_Request("There must be a category for the place")
        address = request_body.get("address", None)
        if not address:
            raise Bad_Request("There must be an address for the place")
        city = request_body.get("city", None)
        if not city:
            raise Bad_Request("There must be a city for the place")
        state = request_body.get("state", None)
        if not state:
            raise Bad_Request("There must be a state for the place")
        country = request_body.get("country", None)
        if not country:
            raise Bad_Request("There must be a country for the place")
        latitude = request.get("latitude", None)
        longitude = request.get("longitude", None)

        place = Place(creator_id=user_id,
                      name=name,
                      category=category,
                      description=description,
                      address=address,
                      city=city,
                      state=state,
                      country=country,
                      latitude=latitude,
                      longitude=longitude)
        storage.new(place)
        storage.save()
        return JSONResponse(content=place.to_dict(), status_code=status.HTTP_201_CREATED)
    raise Unauthorized()

@place_router.put("/places/{place_id}")
async def edit_place(place_id: str, request: Request) -> str:
    """PUT method to edit the information of a place"""
    from models import storage
    if not place_id:
        return Not_Found()
    if not request:
        return Bad_Request()
    if request.state.current_user:
        if request.state.current_user.role == "user":
            raise Unauthorized("You are not allowed to perform this operation")
        user_id = request.state.current_user.id
        # user_role = request.state.current_user.role
        try:
            request_body = await request.json()
        except Exception:
            raise Bad_Request()
        
        place = storage.search_key_value("Place", "id", place_id)
        if not place:
            raise Not_Found("Place not found")
        if request.state.current_user.role == "user":
            raise Unauthorized("You can't perform this action")
        
        if "creator_id" in request_body:
            raise Unauthorized("You are not allowed to change the creator_id")
        place[0].recently_updated_by = user_id
        if "name" in request_body:
            place[0].name = request_body["name"]
        if "category" in request_body:
            place[0].category = request_body["category"]
        if "description" in request_body:
            place[0].description = request_body["description"]
        if "address" in request_body:
            place[0].address = request_body["address"]
        if "city" in request_body:
            place[0].city = request_body["city"]
        if "state" in request_body:
            place[0].state = request_body["state"]
        if "country" in request_body:
            place[0].country = request_body["country"]
        if "latitude" in request_body:
            place[0].latitude = request_body["latitude"]
        if "longitude" in request_body:
            place[0].longitude = request_body["longitude"]
        place[0].save()
        return JSONResponse(content=place[0].to_dict(), status_code=status.HTTP_200_OK)
    raise Unauthorized()


@place_router.get("/places/average_rating/{place_id}")
def get_place_average_rating(request: Request, place_id: str = None) -> str:
    """GET method that returns the average rating of a place"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not place_id:
        raise Not_Found("Place not found")
    if not request.state.current_user:
        raise Unauthorized()
    place = storage.search_key_value("Place", "id", place_id)
    if not place:
        raise Not_Found("Place not found")
    reviews = storage.search_key_value("Review", "place_id", place_id)
    if not reviews:
        return JSONResponse(content={"message": "No reviews for this place"}, status_code=status.HTTP_404_NOT_FOUND)
    total = 0
    for review in reviews:
        total += review.rating
    average_rating = total / len(reviews)
    return JSONResponse(content={"average_rating": average_rating}, status_code=status.HTTP_200_OK)



@place_router.get("/places/all_reviews/{place_id}")
def get_all_reviews_of_place(request: Request, place_id: str = None) -> str: