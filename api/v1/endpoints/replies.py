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


@replies_router.get("/replies/{reply_id}")
def get_a_reply(request: Request, reply_id: str = None) -> str:
    """GET method for a particular reply"""
    from models import storage
    if not request:
        return Bad_Request()
    if not reply_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    reply = storage.search_key_value("Reply", "id", reply_id)
    if not reply:
        raise Not_Found("This reply does not exist")
    reply = reply[0]
    return JSONResponse(content=reply.to_dict(), status_code=status.HTTP_200_OK)


@replies_router.delete("/replies/{reply_id}")
def delete_a_reply(request: Request, reply_id: str = None) -> str:
    """DELETE method that deletes a reply"""
    from models import storage
    if not request:
        return Bad_Request()
    if not reply_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    user = request.state.current_user
    reply = storage.search_key_value("Reply", "id", reply_id)
    if user.role == "user":
        if reply[0].user_id != user.id:
            raise Unauthorized("You are not authorized to perform this operation")
    storage.delete(reply[0])
    storage.save()
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


