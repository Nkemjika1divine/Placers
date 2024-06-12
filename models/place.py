#!/usr/bin/python3
"""The Place Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Place(BaseModel, Base):
    """The Place model"""