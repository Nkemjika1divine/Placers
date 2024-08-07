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
            raise Not_Found("No place in the database yet")
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
        if request.state.current_user.role == 'user':
            raise Unauthorized("You are not authorized to perform this operation")
        user_id = request.state.current_user.id
        try:
            request_body = await request.json()
        except Exception as e:
            raise Bad_Request(f"Request body not processed properly. Reason: {e}")
        # get name
        name = request_body.get("name", None)
        if not name or type(name) is not str:
            raise Bad_Request("name missing or not str")
        # get and validate category
        category = request_body.get("category", None)
        if not category or type(category) is not str:
            raise Bad_Request("category missing or not a string")
        list_of_categories = storage.all("Category")
        if not list_of_categories:
            raise Unauthorized("No category in the database yet")
        for value in list_of_categories.values():
            if value.category_name == category:
                category_id = value.id
                break
        if not category_id:
            raise Bad_Request("Category not found in the database")
        # get description
        description = request_body.get("description", None)
        if description and type(description) is not str:
            raise Bad_Request("description must be a string")
        # get address
        address = request_body.get("address", None)
        if not address or type(address) is not str:
            raise Bad_Request("address missing or not a string")
        # get city
        city = request_body.get("city", None)
        if not city or type(city) is not str:
            raise Bad_Request("city missing or not str")
        # get state
        state = request_body.get("state", None)
        if not state or type(state) is not str:
            raise Bad_Request("state missing or not a string")
        # get country
        country = request_body.get("country", None)
        if not country or type(country) is not str:
            raise Bad_Request("country missing or not a string")
        # get latitude
        latitude = request.get("latitude", None)
        if latitude and type(latitude) is not str:
            raise Bad_Request("latitude must be a float")
        # get longitude
        longitude = request.get("longitude", None)
        if longitude and type(longitude) is not str:
            raise Bad_Request("longitude must be a float")

        place = Place(creator_id=user_id,
                      name=name,
                      category_id=category_id,
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
        except Exception as e:
            raise Bad_Request(f"There's a problem with the request body. Reason {e}")
        
        place = storage.search_key_value("Place", "id", place_id)
        if not place:
            raise Not_Found("Place not found")
        
        if "creator_id" in request_body:
            raise Unauthorized("You are not allowed to change the creator_id")
        place[0].recently_updated_by = user_id
        if "name" in request_body:
            if type(request_body['name']) is not str:
                raise Bad_Request("name must be a string")
            place[0].name = request_body["name"]
        if "category" in request_body:
            if type(request_body['category']) is not str:
                raise Bad_Request("category must be a string")
            list_of_categories = storage.all("Category")
            if not list_of_categories:
                raise Unauthorized("no categories in the database yet")
            for value in list_of_categories.values():
                if value.category_name == request_body['category']:
                    category_id = value.id
                    break
            place[0].category_id = category_id
        if "description" in request_body:
            if type(request_body['description']) is not str:
                raise Bad_Request("description must be a string")
            place[0].description = request_body["description"]
        if "address" in request_body:
            if type(request_body['address']) is not str:
                raise Bad_Request("address must be a string")
            place[0].address = request_body["address"]
        if "city" in request_body:
            if type(request_body['city']) is not str:
                raise Bad_Request("city must be a string")
            place[0].city = request_body["city"]
        if "state" in request_body:
            if type(request_body['state']) is not str:
                raise Bad_Request("state must be a string")
            place[0].state = request_body["state"]
        if "country" in request_body:
            if type(request_body['country']) is not str:
                raise Bad_Request("country must be a string")
            place[0].country = request_body["country"]
        if "latitude" in request_body:
            if type(request_body['latitude']) is not str:
                raise Bad_Request("latitude must be a float")
            place[0].latitude = request_body["latitude"]
        if "longitude" in request_body:
            if type(request_body['longitude']) is not str:
                raise Bad_Request("longitude must be a float")
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
    average_rating = place.get_average_rating()
    if average_rating == 0:
        raise Not_Found(f"no ratings for this {place.name} yet")
    return JSONResponse(content={"average_rating": average_rating}, status_code=status.HTTP_200_OK)


@place_router.get("/places/all_reviews/{place_id}")
def get_all_reviews_of_place(request: Request, place_id: str = None) -> str:
    """GET method to retrieve all reviews of a place"""
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
        raise Not_Found("No reviews for this place")
    review_list = []
    for review in reviews:
        review_json = review.to_dict()
        review_list.append(review_json)
    return JSONResponse(content=review_json, status_code=status.HTTP_200_OK)


@place_router.get("/places/{place_id}/like_details")
def get_like_details(request: Request, place_id: str = None) -> str:
    """GET method that returns the number of likes a place has and the percentage likes"""
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
        raise Not_Found("No reviews for this place")
    id_count = 0
    like_count = 0
    for review in reviews:
        id_count += 1
        if review.like == "yes":
            like_count += 1
    percentage = (like_count/id_count) * 100
    return JSONResponse(content={"likes": like_count, "percentage_of_likes": percentage}, status_code=status.HTTP_200_OK)


@place_router.get("/places/places_by_category")
async def search_places_by_category(request: Request) -> str:
    """GET method that searches for places by category"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception as e:
        raise Bad_Request(f"Error: {e}")
    if 'category' in request_body:
        if type(request_body['category']) is not str:
            raise Bad_Request('category must be a string')
        all_categories = storage.all("Category")
        if not all_categories:
            raise Not_Found(f"{request_body['category']} not found")
        for category in all_categories:
            if category.category_name == request_body['category']:
                all_places = storage.search_key_value("Place", "category_id", category.id)
                if not all_places:
                    raise Not_Found(f"No place found for this category {request_body['category']}")
                return JSONResponse(content=all_places, status_code=status.HTTP_200_OK)
    raise Bad_Request("no category in the request")