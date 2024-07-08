#!/usr/bin/python3
"""The /users endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized
from models.review import Review


review_router = APIRouter()


@review_router.get("/reviews")
def get_all_reviews(request: Request) -> str:
    """GET method to retrieve all reviews"""
    from models import storage
    if not request:
        return Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    all_reviews = []
    get_all_reviews = storage.all("Review")
    for value in get_all_reviews.values():
        all_reviews.append(value.to_dict())
    return JSONResponse(content=all_reviews, status_code=status.HTTP_200_OK)


