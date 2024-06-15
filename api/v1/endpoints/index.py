#!/usr/bin/python3
"""Module conntaining index endpoints"""
from api.v1.app import app
from fastapi import APIRouter


index_router = APIRouter()


@index_router.get("/status")
def status():
    """Returns the status of the API"""
    return {"status": "ok"}


app.include_router(index_router, prefix="/api/v1")