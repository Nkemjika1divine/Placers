#!/usr/bin/python3
"""Module containing error handling classes"""
from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class Unauthorized(HTTPException):
    """Handles Unauthorized access"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_401_UNAUTHORIZED,
                         detail=f"error: {detail}" if detail else {"error": "Unauthorized"})


class Forbidden(HTTPException):
    """Handles Forbidden access"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_403_FORBIDDEN,
                         detail=f"error: {detail}" if detail else {"error": "Forbidden"})

class Not_Found(HTTPException):
    """Handles Not found error"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND,
                         detail=f"error: {detail}" if detail else {"error": "Not Found"})

class Bad_Request(HTTPException):
    """Handles Bad requests or incomplete request"""
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=HTTP_400_BAD_REQUEST,
                         detail=f"error: {detail}" if detail else {"error": "Incomplete Request"})