#!/usr/bin/python3
"""Module deploying our FastAPI app"""
from fastapi import FastAPI, APIRouter
# from api.v1.endpoints.index import index_router


app = FastAPI()


index_router = APIRouter()


api_prefix = "/api/v1"


app.include_router(index_router, prefix=api_prefix)