#!/usr/bin/python3
"""Module deploying our FastAPI app"""
import os
from api.v1.endpoints.index import index_router
from api.v1.error_handlers import Unauthorized, Forbidden
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
api_prefix = "/api/v1"
app.include_router(index_router, prefix=api_prefix)

path_list = ['/api/v1/status/', '/api/v1/forbidden/', '/api/v1/unauthorized/']


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # URLs to allow
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE all allowed
    allow_headers=["*"]  # All headers allowed
)
auth = None
if os.environ.get("AUTH_TYPE") == "auth":
    from auth.auth import Auth
    auth = Auth()


"""@app.route("/{any_path:path}")
def return_the_path(any_path: str) -> str:
    """"Checks the url entered by the user and returns the endpoint"""""
    if any_path:
        if any_path[0:22] == "https://localhost:8000":
            return any_path[22:]
        elif any_path[0:21] == "http://localhost:8000":
            return any_path[21:]"""


def get_request_header(request: Request):
    """Accesses header in the user's request"""
    return request.headers



@app.route("/{any_path:path}")
def authentication(any_path: str) -> str:
    if not auth:
        return
    if any_path:
        if any_path[0:22] == "https://localhost:8000":
            if auth.require_auth(any_path[22:], path_list):
                if not auth.authorization_header(get_request_header()):
                    return Unauthorized()
                if not auth.current_user():
                    return Forbidden()
        elif any_path[0:21] == "http://localhost:8000":
            if auth.require_auth(any_path[22:], path_list):
                if not auth.authorization_header(get_request_header()):
                    return Unauthorized()
                if not auth.current_user():
                    return Forbidden()
    
    