# api/app.py
from fastapi import FastAPI
from api.routes.generate import router as generate_router
from api.routes.health import router as health_router

app = FastAPI(title="Kids Video Factory")

app.include_router(generate_router)
app.include_router(health_router)