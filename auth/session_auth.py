#!/usr/bin/python3
"""Module for session authentication"""
from fastapi import Request
from auth.auth import Auth
from models.session import Session
from uuid import uuid4
from typing import TypeVar

class SessionAuth(Auth):
    """Handles session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creaates a session ID for a user"""
        from models import storage
        if user_id is None or type(user_id) is not str:
            return None
        user = storage.get_user(user_id)
        if user:
            session = Session()
            session.user_id = user_id
            session.save()
            return session.id
        return None
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user based on Session ID"""
        from models import storage
        if session_id is None or type(session_id) is not str:
            return None
        session = storage.search_key_value("Session", "id", session_id)
        if session:
            return session[0].user_id
        return None
    
    def check_db_current_user(self, request: Request) -> TypeVar("User"):
        """Checks if a request is from a current user in the database and returns the user"""
        from models import storage
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        session = storage.search_key_value("Session", "id", session_id)
        if not session:
            return None
        user = storage.search_key_value("User", "id", session[0].user_id)
        if not user:
            return None
        return user[0]
    
    def current_user(self, request: Request) -> TypeVar("User"):
        """Returns a user instance based on cookie value"""
        from models import storage
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        session = storage.search_key_value("Session", "id", session_id)
        if not session:
            return None
        user = storage.search_key_value("User", "id", session[0].user_id)
        if not user:
            return None
        return user[0]
    
    def destroy_session(self, request: Request) -> bool:
        """Deletes a sesssion"""
        from models import storage
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        session = storage.search_key_value("Session", "id", session_id)
        if not session:
            return None
        user = storage.search_key_value("User", "id", session[0].user_id)
        if not user:
            return None
        storage.delete(user[0])
        storage.save
        return True
    
    