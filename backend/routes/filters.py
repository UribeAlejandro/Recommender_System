import logging

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from backend.routes.utils import get_all_applicable_pets

router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.get("/applicable_pets", status_code=200, response_class=ORJSONResponse)
def all_applicable_pets():
    """
    Get all applicable pets.

    Returns
    -------
    dict
        The applicable pets
    """
    logger.info("Getting all applicable pets...")
    all_applicable_pets_list = get_all_applicable_pets()
    return ORJSONResponse(all_applicable_pets_list)
