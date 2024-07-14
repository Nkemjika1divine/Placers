#!/usr/bin/python3
"""The Category module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Category(BaseModel, Base):
    """The category class"""
    __tablename__ = "categories"
    category = Column(String(29), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)