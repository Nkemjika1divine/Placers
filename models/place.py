#!/usr/bin/python3
"""The Place Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float


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
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)