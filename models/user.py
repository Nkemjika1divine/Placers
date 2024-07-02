#!/usr/bin/python3
"""The User module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property
import hashlib
import hmac
import os


class User(BaseModel, Base):
    """The User model"""
    __tablename__ = "users"
    name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    _hashed_password = Column("hashed_password", String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @hybrid_property
    def hashed_password(self) -> str:
        """ Getter of the password"""
        return self._hashed_password

    @hashed_password.setter
    def hashed_assword(self, password: str = None):
        """Hashes the password and returns the hashed version"""
        if password is None or type(password) is not str:
            raise ValueError("Password must be a string")
        self._hashed_password = self.hash_password(password)

    def hash_password(self, password: str = None) -> str:
        """Hashes a user's password"""
        if not password or type(password) is not str:
            return None
        return hashlib.sha256(password.encode()).hexdigest().lower()
    
    def is_valid_password(self, password: str = None) -> bool:
        """Verifies to ensure that password entered is the same in the DB"""
        if not password or type(password) is not str:
            return False
        if self._hashed_password is None:
            return False
        password_e = password.encode()
        return hashlib.sha256(password_e).hexdigest().lower() == self._hashed_password
    
    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.email is None and self.username is None:
            return ""
        else:
            return "{} (@{})".format(self.name, self.username)