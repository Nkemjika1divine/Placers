#!/usr/bin/python3
"""Module containing error handling classes"""
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class Unauthorized(HTTPException):
    """Handles Unauthorized access"""
    def __init__(self):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail={"error": "Unauthorized"})
