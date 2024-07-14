#!/usr/bin/python3
"""The Place Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float


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