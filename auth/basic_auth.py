#!/usr/bin/python3
"""Basic Authentication module"""
from auth.auth import Auth
from models.user import User
from typing import TypeVar
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
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract the credentials of the user"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' in decoded_base64_authorization_header:
            email_password = decoded_base64_authorization_header.split(":")
            email = email_password[0]
            password = ':'.join(email_password[1:])
            return email, password
        return None, None
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Extracts the user object from the credentials"""
        from models import storage
        if not user_email:
            return None
        if not user_pwd:
            return None
        if type(user_pwd) is not str or type(user_email) is not str:
            return None
        try:
            print("Searhing for email")
            user = storage.search_key_value(classname="User", key="email", value=user_email)
        except KeyError:
            print("key error")
            return None
        if not user:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]
    
    async def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user"""
        auth = self.authorization_header(request)
        extract = self.get_base64_authorization_header(auth)
        decoded = self.decode_base64_authorization_header(extract)
        email, password = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, password)