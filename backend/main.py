import logging

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from backend.constants import DATABASE_NAME, MONGO_URI
from backend.models import __beanie_models__
from backend.routes import ping, products, reviews, user

logger = logging.getLogger("uvicorn")

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Startup event."""
    logger.info("Starting up...")

    logger.info("Adding DB connection...")
    client = AsyncIOMotorClient(MONGO_URI)

    logger.info("Setting up Beanie...")
    await init_beanie(database=client[DATABASE_NAME], document_models=__beanie_models__)

    logger.info("Setting up routes...")
    app.include_router(ping.router)
    app.include_router(user.router)
    app.include_router(reviews.router)
    app.include_router(products.router, tags=["products"])


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event."""
    logger.info("Shutting down...")
