#!/usr/bin/python3
"""Utility module"""
from fastapi import Request, Depends


async def get_request_header(request: Request):
    """Accesses header in the user's request"""
    if request:
        return request.headers
    else:
        print("Nothing in request")
        return