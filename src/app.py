import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.views.health import router as health_router
from src.views.analitics import router as analitics_router
from src import models

load_dotenv()

def create_app():
    app = FastAPI(title="Redis statistic")
    app.secret_key = os.getenv("SECRET_KEY")

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        health_router,
        prefix="/api",
        tags=["Health"]
    )

    app.include_router(
        analitics_router,
        prefix="/api",
        tags=["Analitic"]
    )


    return app
