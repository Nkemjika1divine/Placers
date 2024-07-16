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
    if not review_id:
        raise Not_Found()
    if not request.state.current_user:
        raise Unauthorized()
    review = storage.search_key_value("Review", "id", review_id)
    if not review:
        raise Not_Found("This review does not exist")
    review = review[0]
    return JSONResponse(content=review.to_dict(), status_code=status.HTTP_200_OK)



@review_router.post("/{place_id}/reviews")
async def add_a_review(request: Request, place_id: str = None) -> str:
    """POST method to add a new review"""
    from models import storage
    print("in post reviews")
    if not place_id:
        return Not_Found("Place does not exist")
    if not request:
        return Bad_Request()
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request("Error parsing request")
    
    place = storage.search_key_value("Place", "id", place_id)
    if not place:
        raise Not_Found("Place does not exist")
    place = place[0]

    user_id = request.state.current_user.id
    place_id = place.id
    rating = request_body.get("rating", None)
    if not rating or type(rating) is not int or rating > 10 or rating < 0:
        raise Bad_Request("rating missing and must be a whole number from 0 to 10")
    full_review = request_body.get("full_review", None)
    if type(full_review) is not str:
        raise Bad_Request("full_review must be a string")
    like = request_body.get("like", None)
    if type(like) is not str:
        raise Bad_Request("like must be a string")

    review = Review(user_id=user_id, place_id=place_id, rating=rating, full_review=full_review)
    storage.new(review)
    storage.save()
    return JSONResponse(content=review.to_dict(), status_code=status.HTTP_201_CREATED)


@review_router.put("/reviews/{review_id}")
async def edit_a_review(request: Request, review_id: str = None) -> str:
    """PUT method to edit a review"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not review_id:
        raise Not_Found("Review not found")
    if not request.state.current_user:
        raise Unauthorized()
    try:
        request_body = await request.json()
    except Exception:
        raise Bad_Request()
    review = storage.search_key_value("Review", "id", review_id)
    if not review:
        raise Not_Found("Review does not exist")
    review = review[0]
    if review.user_id != request.state.current_user.id:
        raise Unauthorized("You are not allowed to perform this operation")
    if 'rating' in request_body:
        if type(request_body["rating"]) is not int or request_body["rating"] > 10 or request_body["rating"] < 0:
            raise Unauthorized("Rating must be a whole number from 0 to 10")
        review.rating = request_body["rating"]
    if "full_review" in request_body:
        review.full_review = request_body["full_review"]
    review.save()
    return JSONResponse(content=review.to_dict(), status_code=status.HTTP_200_OK)


@review_router.delete("/reviews/{review_id}")
def delete_a_review(request: Request, review_id: str = None) -> str:
    """DELETE method to delete a review"""
    from models import storage
    if not request:
        raise Bad_Request()
    if not review_id:
        raise Not_Found("Review not found")
    if not request.state.current_user:
        raise Unauthorized()
    review = storage.search_key_value("Review", "id", review_id)
    if not review:
        raise Not_Found("Review not found")
    review = review[0]
    if review.user_id != request.state.current_user.id:
        if request.state.current_user.role == 'user':
            raise Unauthorized("You are not allowed to perform this operation")
    storage.delete(review)
    storage.save
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


