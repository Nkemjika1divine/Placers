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

@place_router