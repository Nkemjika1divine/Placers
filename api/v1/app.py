#!/usr/bin/python3
"""Module deploying our FastAPI app"""
import os
from api.v1.endpoints.index import index_router
from api.v1.error_handlers import Unauthorized, Forbidden
from auth.middleware.middleware import AuthMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


load_dotenv()

app = FastAPI()
api_prefix = "/api/v1"
app.include_router(index_router, prefix=api_prefix)

path_list = ['/api/v1/status', '/api/v1/forbidden', '/api/v1/unauthorized']


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # URLs to allow
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE all allowed
    allow_headers=["*"]  # All headers allowed
)

@app.exception_handler(Unauthorized)
async def unauthorized_handler(request: Request, exc: Unauthorized):
    """Handles Unauthorized exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.exception_handler(Forbidden)
async def forbidden_handler(request: Request, exc: Forbidden):
    """Handles Forbidden exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )






auth = None
if os.environ.get("AUTH_TYPE") == 'auth':
    from auth.auth import Auth
    auth = Auth()

if auth:
    app.add_middleware(AuthMiddleware, auth=auth, excluded_paths=path_list)


"""@app.add_exception_handler(Unauthorized, unauthorized_handler)
@app.add_exception_handler(Forbidden, forbidden_handler)"""