#!/usr/bin/python3
"""The categories endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized


categories_router = APIRouter()


@categories_router.get("/categories")
def get_all_categories(request: Request):
    """GET request that returns all categories"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role == 'user':
        raise Unauthorized("You are not allowed to perform this operation")
    categories = storage.all("Category")
    if not categories:
        raise Not_Found("No categories in the Database")
    all_categories =  []
    for value in categories.values():
        all_categories.append(value.to_dict())
    return JSONResponse(content=all_categories, status_code=status.HTTP_200_OK)