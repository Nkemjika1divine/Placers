#!/usr/bin/python3
"""The Place Module"""
from decimal import Decimal
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, CheckConstraint


"""categories = ["Religious institution",
              "School",
              "Park",
              "Hotel",
              "Restaurant",
              "Museum",
              "Farm",
              "Industry",
              "Studio",
              "Beach",
              "Club"]"""


class Place(BaseModel, Base):
    """The Place model"""
    __tablename__ = "places"
    creator_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    address = Column(String(250), nullable=False, unique=True)
    longitude = Column(Decimal(10, 6), nullable=True)
    latitude = Column(Decimal(10, 6), nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)