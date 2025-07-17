from fastapi import FastAPI

from src.exceptions.handler import register_exception
from .routes.course_routes import course_router


app = FastAPI(title="Summoners school")

register_exception(app)
app.include_router(course_router,prefix='/course' , tags=["Course Routes"])
