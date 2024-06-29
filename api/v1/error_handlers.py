#!/usr/bin/python3
"""Module containing error handling classes"""
from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


class Unauthorized(HTTPException):
    """Handles Unauthorized access"""
    def __init__(self) -> None:
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail={"error": "Unauthorized"})


class Forbidden(HTTPException):
    """Handles Forbidden access"""
    def __init__(self) -> None:
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail={"error": "Forbidden"})