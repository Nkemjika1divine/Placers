#!/usr/bin/python3
"""Module conntaining index endpoints"""
from api.v1.app import index_router


@index_router.get("/status")
def status():
    """Returns the status of the API"""
    return {"status": "ok"}