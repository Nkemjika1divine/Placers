#!/usr/bin/python3
"""Basic authentication module"""
from typing import List, TypeVar


class Auth:
    """Authehtication class"""

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
                            else:
                                return True
        return False
    
    def authorization_header(self, request=None) -> str:
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        return None