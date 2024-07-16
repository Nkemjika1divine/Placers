#!/usr/bin/python3
"""The categories endpoint module"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Not_Found, Bad_Request, Unauthorized
from models.reply import Reply


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
    if not reply:
        raise Not_Found("reply not found")
    if user.role == "user":
        if reply[0].user_id != user.id:
            raise Unauthorized("You are not authorized to perform this operation")
    storage.delete(reply[0])
    storage.save()
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@replies_router.post("/replies/{review_id}/")
async def post_a_new_reply(request: Request, review_id: str = None) -> str:
    """POST method that adds a new reply to a review"""
    from models import storage
    if not request:
        return Bad_Request()
    if not review_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    review = storage.search_key_value("Review", "id", review_id)
    if not review:
        raise Not_Found("review not found")
    try:
        body = await request.json()
    except Exception as e:
        raise Bad_Request(f"Error: {e}")
    user_id = request.state.current_user.id
    full_reply = body.get("reply", None)
    if not full_reply or type(full_reply) is not str:
        raise Bad_Request("full_reply missing or not a string")
    
    reply = Reply(review_id=review_id, user_id=user_id, full_reply=full_reply)
    reply.save()
    return JSONResponse(content=reply.to_dict(), status_code=status.HTTP_201_CREATED)