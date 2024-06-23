#!/usr/bin/python3
"""Module deploying our FastAPI app"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from api.v1.endpoints.index import index_router


app = FastAPI()
api_prefix = "/api/v1"


app.include_router(index_router, prefix=api_prefix)