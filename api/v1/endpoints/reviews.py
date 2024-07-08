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


@review_router.get("/reviews/{review_id}")
def get_a_review(request: Request, review_id: str = None) -> str:
    """GET method for retreiving a user"""
    from models import storage
    if not request:
        return Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    review = storage.search_key_value("Review", "id", review_id)
    if not review:
        raise Not_Found("This review does not exist")
    review = review[0]
    return JSONResponse(content=review.to_dict(), status_code=status.HTTP_200_OK)



@review_router.post("/reviews/{place_id}")
async def add_a_review(request: Request, place_id: str = None) -> str:
    """POST method to add a new route"""
    from models import storage
    if not place_id:
        return Not_Found("Place does not exist")
    if not request:
        return Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request()
    
    place = storage.search_key_value("Place", "id", place_id)
    if not place:
        raise Not_Found("Place does not exist")
    place = place[0]

    user_id = request.state.current_user.id
    place_id = place.id
    rating = request_body.get("rating", None)
    if not rating or type(rating) is not int or rating > 10 or rating < 0:
        raise Bad_Request("Rating must be added, and must be a whole number from 0 to 10")
    full_review = request_body.get("full_review", None)

    review = Review(user_id=user_id, place_id=place_id, rating=rating, full_review=full_review)
    storage.new(review)
    storage.save()
    return JSONResponse(content=review.to_dict(), status_code=status.HTTP_201_CREATED)