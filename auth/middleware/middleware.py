#!/usr/bin/python3
""" Module Handles middleware operations"""
from api.v1.error_handlers import Unauthorized, Forbidden
from auth.auth import Auth
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from typing import List


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware"""

    def __init__(self, app, auth, excluded_paths: List[str]):
        """'Handles Initialization of the middleware'"""
        super().__init__(app)
        self.auth = auth
        self.excluded_paths = excluded_paths
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """This performs evaluation of request before route operations"""
        path = request.url.path
        try:
            if self.auth.require_auth(path, self.excluded_paths):
                authorization = await self.auth.authorization_header(request)
                if not authorization:
                    raise Unauthorized()
                if not self.auth.current_user():
                    raise Forbidden()
            response = await call_next(request)
        except Unauthorized as e:
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail
            )
        except Forbidden as e:
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail
            )
        return response