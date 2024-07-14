import logging

from beanie.operators import Eq
from fastapi import APIRouter
from pymongo import DESCENDING

from backend.models.Collections import ProductReview

router = APIRouter(prefix="/user", redirect_slashes=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


@router.get("/reviews", status_code=200)
async def get_reviews(nickname: str):
    """
    Get reviews.

    Returns
    -------
    dict
        The reviews
    """
    reviews = (
        await ProductReview.find(Eq(ProductReview.nickname, nickname))
        .sort([(ProductReview.timestamp, DESCENDING)])
        .to_list()
    )

    return reviews
