#!/usr/bin/python3
"""The Session Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Session(BaseModel, Base):
    """The Reply model"""
    __tablename__ = "session_table"
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)