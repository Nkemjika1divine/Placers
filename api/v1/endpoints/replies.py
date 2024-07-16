#!/usr/bin/python3
"""The categories endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized
from models.category import Category


replies_router = APIRouter()


@replies_router.get("/replies")
def get_all_replies(request: Request) -> str:
    """GET method to return all replies in the database"""
    from models import storage
    if not request:
        return Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    all_replies = []
    get_all_replies = storage.all("Reply")
    for value in get_all_replies.values():
        all_replies.append(value.to_dict())
    return JSONResponse(content=all_replies, status_code=status.HTTP_200_OK)