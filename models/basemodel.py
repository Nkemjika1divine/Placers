#!/usr/bin/python3
"""The BaseModel Module"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime


class BaseModel:
    """The BaseModel class"""
    __abstract__ = True
    id = Column(String(50), primary_key=True, nullable=False)
    time_created = Column(DateTime, default=datetime.now, nullable=False)
    time_updated = Column(DateTime, default=datetime.now, nullable=False)