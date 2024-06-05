import logging

from fastapi import FastAPI

from backend.routes import ping

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
