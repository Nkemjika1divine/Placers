#!/usr/bin/python3
"""The Category module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Category(BaseModel, Base):
    """The Category model"""
    __tablename__ = "categories"
    category = Column(String(50), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)