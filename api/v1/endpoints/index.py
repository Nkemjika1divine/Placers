#!/usr/bin/python3
"""Module conntaining index endpoints"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from api.v1.error_handlers import *
# from starlette.status import HTTP_401_UNAUTHORIZED
# from api.v1.endpoints.index import index_router



index_router = APIRouter()



"""@app.exception_handler(Unauthorized)
def handle_unauthorized():
    return JSONResponse({"error": "Unauthorized"}, status_code=HTTP_401_UNAUTHORIZED)"""



@index_router.get("/status")
def api_status():
    """Returns the status of the API"""
    return JSONResponse({"status": "ok"})

@index_router.get("/unauthorized")
def unauthorized():
    """Raises Error 401 (Unauthorized)"""
    raise Unauthorized()

@index_router.get("/forbidden")
def forbidden():
    """Raises Error 403 (Forbidden)"""
    raise Forbidden()

@index_router.get("/number_of_users")
def number_of_users(request: Request):
    """GET request that returns the number of users in the database"""
    from models import storage
    if not request.state.current_user:
        raise Bad_Request()
    user_count = storage.count("User")
    return JSONResponse(content={"users": user_count}, status_code=status.HTTP_200_OK)

@index_router.get("/number_of_places")
def number_of_places(request: Request):
    """GET request that returns the number of users in the database"""
    from models import storage
    if not request.state.current_user:
        raise Bad_Request()
    place_count = storage.count("Place")
    return JSONResponse(content={"places": place_count}, status_code=status.HTTP_200_OK)