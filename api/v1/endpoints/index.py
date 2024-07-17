#!/usr/bin/python3
"""Module conntaining index endpoints"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import *


index_router = APIRouter()


@index_router.get("/status")
def api_status():
    """Returns the status of the API"""
    return JSONResponse({"status": "ok", "api version": "v1.0.0"}, status_code=status.HTTP_200_OK)

@index_router.get("/unauthorized")
def unauthorized():
    """Raises Error 401 (Unauthorized)"""
    raise Unauthorized()

@index_router.get("/forbidden")
def forbidden():
    """Raises Error 403 (Forbidden)"""
    raise Forbidden()

@index_router.get("/number_of_users")
def number_of_users(request: Request):
    """GET request that returns the number of users in the database"""
    from models import storage
    if not request.state.current_user:
        raise Unauthorized()
    user_count = storage.count("User")
    return JSONResponse(content={"users": user_count}, status_code=status.HTTP_200_OK)

@index_router.get("/number_of_places")
def number_of_places(request: Request):
    """GET request that returns the number of users in the database"""
    from models import storage
    if not request.state.current_user:
        raise Unauthorized()
    place_count = storage.count("Place")
    return JSONResponse(content={"places": place_count}, status_code=status.HTTP_200_OK)

@index_router.get("/number_of_reviews")
def number_of_reviews(request: Request):
    """GET request that returns the number of users in the database"""
    from models import storage
    if not request.state.current_user:
        raise Unauthorized()
    review_count = storage.count("Review")
    return JSONResponse(content={"reviews": review_count}, status_code=status.HTTP_200_OK)


@index_router.get("/number_of_replies")
def number_of_replies(request: Request):
    """GET request that returns the number of replies in the database"""
    from models import storage
    if not request.state.current_user:
        raise Unauthorized()
    reply_count = storage.count("Reply")
    return JSONResponse(content={"users": reply_count}, status_code=status.HTTP_200_OK)


@index_router.get("/number_of_categories")
def number_of_categories(request: Request):
    """GET request that returns the number of users in the database"""
    from models import storage
    if not request.state.current_user:
        raise Unauthorized()
    categories_count = storage.count("User")
    return JSONResponse(content={"users": categories_count}, status_code=status.HTTP_200_OK)