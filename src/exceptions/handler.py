from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .base_exceptions import BadRequest, NotFoundException


def register_exception(app:FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.detail})
    @app.exception_handler(BadRequest)
    async def bad_req_handler(req:Request , exc : BadRequest):
        return JSONResponse(status_code=400, content={"detail": exc.detail})