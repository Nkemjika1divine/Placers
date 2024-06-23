#!/usr/bin/python3
"""Module conntaining index endpoints"""
#!/usr/bin/python3
"""Module deploying our FastAPI app"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.v1.error_handlers import Unauthorized, Forbidden
# from starlette.status import HTTP_401_UNAUTHORIZED
# from api.v1.endpoints.index import index_router



index_router = APIRouter()



"""@app.exception_handler(Unauthorized)
def handle_unauthorized():
    return JSONResponse({"error": "Unauthorized"}, status_code=HTTP_401_UNAUTHORIZED)"""



@index_router.get("/status")
def status():
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