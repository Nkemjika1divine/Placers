#!/usr/bin/python3
"""Module containing operation for session expiry"""
from fastapi import Request
from auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Class handling session expiry"""
    pass