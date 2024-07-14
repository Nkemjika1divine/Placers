#!/usr/bin/python3
"""The Category module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Category(BaseModel, Base):
    """The Category model"""
    __tablename__ = "categories"
    category_name = Column(String(50), nullable=False, unique=True)
    user_who_added_category = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_who_updated_category = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)