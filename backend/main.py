import logging

from fastapi import FastAPI

from backend.routes import filters, ping, products, reviews

log = logging.getLogger("uvicorn")


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
    application.include_router(filters.router)
    application.include_router(products.router)
    application.include_router(reviews.router)

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    """Startup event."""
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event."""
    log.info("Shutting down...")
