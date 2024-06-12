#!/usr/bin/python3
"""The Place Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, DECIMAL


class Place(BaseModel, Base):
    """The Place model"""
    __tablename__ = "places"
    creator_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    address = Column(String(250), nullable=False, unique=True)
    longitude = Column(DECIMAL(10, 6), nullable=True)
    latitude = Column(DECIMAL(10, 6), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)