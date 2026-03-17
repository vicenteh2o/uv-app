from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="FastAPI + uv")

app.include_router(router)
