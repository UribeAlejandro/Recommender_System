import logging

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("uvicorn")


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
