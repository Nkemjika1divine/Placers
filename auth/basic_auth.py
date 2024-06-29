#!/usr/bin/python3
"""Basic Authentication module"""
from auth.auth import Auth


class BasicAuth(Auth):
    """The Basic Auth Class"""
    
    def get_base64_authorization_header(self, authorization_header: str) -> str:
        """Returns the base64 part of the authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[0:6] == "Basic ":
            return authorization_header[6:]
        return None
    
    