#!/usr/bin/python3
"""The Reply Module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float
from typing import TypeVar

"""
- review_id = the id of the review being replied
- user_id = the user replying the review
- reply = the content of the reply itself
"""


class Reply(BaseModel, Base):
    """The Reply model"""
    __tablename__ = "replies"
    review_id = Column(String(50), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reply = Column(String(200), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)