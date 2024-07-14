#!/usr/bin/python3
"""The categories endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized
from models.category import Category


categories_router = APIRouter()


@categories_router.get("/categories")
def get_all_categories(request: Request):
    """GET method that returns all categories"""
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

@categories_router.get("/categories/names")
def get_category_names(request: Request):
    """GET method that returns only the names of the categories"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    categories = storage.all("Category")
    if not categories:
        raise Not_Found("No categories in the Database")
    all_categories = []
    for value in categories.values():
        all_categories.append(value.category_name)
    return JSONResponse(content=all_categories, status_code=status.HTTP_200_OK)

@categories_router.post("/categories")
async def add_new_category(request: Request):
    """Adds a new category to the database"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    if request.state.current_user.role == 'user':
        raise Unauthorized("You are not allowed to perform this operation")
    user_id = request.state.current_user.id
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request()
    name = request_body.get("category_name", None)
    if not name or type(name) is not str:
        raise Bad_Request("category_name missing or not a string")
    
    new_category = Category()
    new_category.category_name = name
    new_category.user_who_added_category = user_id
    new_category.save()
    return JSONResponse(content=new_category.to_dict(), status_code=status.HTTP_201_CREATED)
