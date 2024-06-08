import logging

from fastapi import FastAPI

from backend.routes import filters, ping, products, reviews, user

logger = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    """
    Create the FastAPI application.

    Returns
    -------
    FastAPI
        The FastAPI application
    """
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(user.router)
    application.include_router(filters.router)
    application.include_router(reviews.router)
    application.include_router(products.router)

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    """Startup event."""
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event."""
    logger.info("Shutting down...")
