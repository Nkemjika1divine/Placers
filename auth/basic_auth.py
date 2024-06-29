#!/usr/bin/python3
"""Basic Authentication module"""
from auth.auth import Auth
import base64


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
    
    def decode_base64_authorization_header(self, base64_header: str) -> str:
        """Decodes the meaning of the base64 part of the authorization header"""
        if not base64_header:
            return None
        if type(base64_header) is not str:
            return None
        try:
            return base64.b64decode(base64_header.encode()).decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None