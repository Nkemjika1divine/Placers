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
                session_id = self.auth.session_cookie(request)
                if session_id:
                    current_user = self.auth.check_db_current_user(request)
                    if current_user:
                        request.state.current_user = current_user
                        print(request.state.current_user)
                        return await call_next(request)
                authorization = await self.auth.authorization_header(request)
                if not authorization:
                    raise Unauthorized()
                current_user = self.auth.current_user(request)
                if not current_user:
                    raise Forbidden()
                request.state.current_user = current_user
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