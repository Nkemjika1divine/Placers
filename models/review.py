#!/usr/bin/python3
"""The Review module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, CheckConstraint, Integer
"""
- user_id = the id of the user posting the review
- place_id = the place the review is for
- rating = the rating given by the user to the place
- full_review = the full review of the user
- like = signifies if the user likes the place
"""


class Review(BaseModel, Base):
    """The Review model"""
    __tablename__ = "reviews"
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(String(50), ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, CheckConstraint("rating >= 0 AND rating <= 10"), nullable=False)
    full_review = Column(String(500), nullable=True)
    like = Column(String(5), nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)