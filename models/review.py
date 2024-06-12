#!/usr/bin/python3
"""The Review module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, CheckConstraint, Integer


class Review(BaseModel, Base):
    """The Review model"""
    __tablename__ = "reviews"
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(String(50), ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, CheckConstraint("rating >= 0 AND rating <= 10"), nullable=False)
    review = Column(String(200), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)