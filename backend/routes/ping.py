from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    """
    Health check endpoint.

    Returns
    -------
    dict
        Health status
    """
    return {"health": "ok"}
