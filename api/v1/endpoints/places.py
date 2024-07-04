#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Unauthorized, Forbidden, Not_Found, Bad_Request
from models.place import Place
from models.user import User
from models import storage


place_router = APIRouter()


@place_router.get("/places")
def get_places():
    """GET /api/v1/users
      - Returns all the places in the database"""
    places = storage.all("Place")
    if not places:
        raise Not_Found()
    all_places = {}
    for key, value in places:
        all_places[key] = value.to_dict()
    return JSONResponse(content=all_places, status_code=status.HTTP_200_OK)

@place_router.get("/places/<place_id>")
def get_a_place(place_id: str = None) -> str:
    """GET request for a particular place"""
    if not place_id:
        raise Not_Found()
    data = storage.all("Place")
    for value in data.values():
        if value.id == place_id:
            return JSONResponse(content=value.to_json(), status_code=status.HTTP_200_OK)
    raise Not_Found()

@place_router.get("/places/search/<keyword>")
def get_a_place(keyword: str = None) -> str:
    """GET request to search for a particular place with a name"""
    if not keyword:
        raise Not_Found()
    place_list = []
    data = storage.all("Place")
    for value in data.values():
        if value.name == keyword:
            place_list.append(value)
        elif value.category == keyword:
            place_list.append(value)
        elif value.address == keyword:
            place_list.append(value)
        elif value.city == keyword:
            place_list.append(value)
        elif value.state == keyword:
            place_list.append(value)
        elif value.country == keyword:
            place_list.append(value)
        return JSONResponse(content=place_list, status_code=status.HTTP_200_OK)
    raise Not_Found()