#!/usr/bin/python3
"""Module for session authentication"""
from fastapi import Request
from auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Handles session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creaates a session ID for a user"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user based on Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id, None)
    
    def current_user(self, request: Request):
        """Returns a user instanc based on cookie value"""
        from models import storage
        if not request:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return storage.get_user(user_id)
    
    def destroy_session(self, request: Request) -> bool:
        """Deletes a sesssion"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
    
    