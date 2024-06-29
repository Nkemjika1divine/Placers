#!/usr/bin/python3
"""Basic authentication module"""
from fastapi import Header, HTTPException, Request, Depends
from typing import Dict, List, TypeVar


class Auth:
    """Authehtication class"""

    async def get_request_header(self, request: Request) -> Dict:
        """Accesses header in the user's request"""
        if request:
            return request.headers
        else:
            return {}

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        -   If path is in excluded_paths, it does not require authentication"""
        if path is None:
            return True
        if not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        else:
            path_with_slash = path + '/'
            if path_with_slash in excluded_paths:
                return False
            else:
                for paths in excluded_paths:
                    if paths[-1] == '*':
                        count = 0
                        for i in paths:
                            count += 1
                            if path[0:count - 1] == paths[0:-1]:
                                return False
                return True
    
    async def authorization_header(self, request: Request) -> str:
        """Retrieves the authorization header from a request"""
        headers = await self.get_request_header(request)
        return headers.get("Authorization", None)
    
    def current_user(self, request=None) -> TypeVar('User'):
        return None