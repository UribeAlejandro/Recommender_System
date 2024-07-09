import logging

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.get("/", status_code=200)
async def get_index() -> str:
    """
    Get index.

    Returns
    -------
    str
        Welcome message
    """
    return "Welcome to the API!"


@router.get("/health")
async def health() -> dict:
    """
    Health check endpoint.

    Returns
    -------
    dict
        Health status
    """
    logger.info("Health check...")
    return {"health": "ok"}
