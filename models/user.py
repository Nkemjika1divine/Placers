#!/usr/bin/python3
"""The User module"""
from models.basemodel import BaseModel, Base
from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy import Column, String, ForeignKey
import re
from uuid import uuid4


class User(BaseModel, Base):
    """The User model"""
    __tablename__ = "users"
    name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    role_updater = Column(String(50), ForeignKey("users.id", ondelete='CASCADE'), nullable=True)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hash_password(self, password: str = None) -> str:
        """Hashes a user's password"""
        if not password or type(password) is not str:
            return None
        return hashpw(password.encode("utf8"), gensalt())
    
    def is_valid_password(self, password: str = None) -> bool:
        """Verifies to ensure that password entered is the same in the DB"""
        if not password or type(password) is not str:
            return False
        if self.password is None:
            return False
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    
    def display_name(self) -> str:
        """ Display User name based on email/username/
        """
        if self.email is None and self.username is None:
            return ""
        else:
            return "{} (@{})".format(self.name, self.username)
    
    def generate_password_token(self, user_id: str = None) -> str:
        """Generated a password token using uuid"""
        from models import storage
        if not user_id or type(user_id) is not str:
            return None
        user = storage.get_user(user_id)
        if not user:
            raise ValueError()
        token = str(uuid4())
        storage.update("User", user_id, reset_token=token)
        return token
    
    def update_password(self, token: str = None, password: str = None) -> None:
        """Updates a user's password"""
        from models import storage
        user = storage.search_key_value("User", "reset_token", token)
        if not user:
            raise ValueError()
        user = user[0]
        storage.update("User", user.id, password=self.hash_password(password), reset_token=None)

    
    def validate_email(self, email: str = None):
        """Validates the user email"""
        from models import storage
        if not email or type(email) is not str:
            return False
        