#!/usr/bin/python3
"""The Database Module"""
from os import environ


class DB:
    """The Database Class
    - Handles all database operations
    """
    __session = None
    __engine = None

    