#!/usr/bin/python3
"""Module deploying our FastAPI app"""
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Unauthorized
from starlette.status import HTTP_401_UNAUTHORIZED
# from api.v1.endpoints.index import index_router


app = FastAPI()
index_router = APIRouter()
api_prefix = "/api/v1"


@app.exception_handler(Unauthorized)
def handle_unauthorized(exc: Unauthorized):
    return JSONResponse({"error": exc.detail}, status_code=HTTP_401_UNAUTHORIZED)



@index_router.get("/status")
def status():
    """Returns the status of the API"""
    return JSONResponse({"status": "ok"})

@index_router.get("/unauthorized")
def unauthorized():
    """Returns a message saying Unauthorized"""
    raise Unauthorized()


app.include_router(index_router, prefix=api_prefix)