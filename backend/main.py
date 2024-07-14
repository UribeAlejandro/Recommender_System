import logging
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from backend.constants import DATABASE_NAME, MONGO_URI
from backend.models import __beanie_models__
from backend.routes import misc, products, recommender, reviews, stats, user
from backend.utils.recommender import get_pinecone_index

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    """
    Create the FastAPI application. This function sets up the routes and lifespan.

    Returns
    -------
    FastAPI
        The FastAPI application
    """
    application = FastAPI(
        title="Recommender API", description="API for the recommender system", version="0.2.0", lifespan=lifespan
    )
    logger.info("Setting up routes...")
    application.include_router(misc.router, tags=["misc"])
    application.include_router(user.router, tags=["user"])
    application.include_router(reviews.router, tags=["reviews"])
    application.include_router(recommender.router, tags=["recommender"])
    application.include_router(stats.router, tags=["stats"])
    application.include_router(products.router, tags=["products"])

    return application


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager:  # noqa
    """
    Set up the database connection and Beanie.

    Parameters
    ----------
    app: FastAPI
        The FastAPI application

    Yields
    ------
    AbstractAsyncContextManager
    """
    logger.info("Setting up lifespan...")
    logger.info("Adding DB connection...")
    client = AsyncIOMotorClient(MONGO_URI)

    logger.info("Setting up Beanie...")
    await init_beanie(database=client[DATABASE_NAME], document_models=__beanie_models__)

    get_pinecone_index()
    yield

    logger.info("Shutting down...")
    logger.info("Closing DB connection...")
    client.close()


app = create_application()
