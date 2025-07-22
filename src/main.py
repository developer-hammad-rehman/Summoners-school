from fastapi import FastAPI
from src.exceptions.handler import register_exception
from .routes import router



app = FastAPI(title="Summoners school")

register_exception(app)
app.include_router(router,prefix='/api')
