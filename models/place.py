#!/usr/bin/python3
"""The Place Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float
from typing import TypeVar


class Place(BaseModel, Base):
    """The Place model"""
    __tablename__ = "places"
    creator_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recently_updated_by_id = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=True)
    name = Column(String(50), nullable=False)
    category_id = Column(String(50), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    address = Column(String(250), nullable=False)
    description = Column(String(200), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    

    def get_average_rating(self) -> float:
        """Retrieves the average rating of a place"""
        from models import storage
        place_id = self.id
        all_reviews = storage.all("Review")
        if not all_reviews:
            return 0
        count = 0
        total_rating = 0
        for review in all_reviews.values():
            if review.place_id == place_id:
                count += 1
                total_rating += review.rating
        return total_rating/count