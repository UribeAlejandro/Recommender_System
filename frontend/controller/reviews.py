import logging
from datetime import datetime

import httpx
import requests

from frontend.constants import BACKEND_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_reviews(product_id: str, nickname: str) -> dict[str, str | dict[str, str]]:
    """
    Get reviews.

    Parameters
    ----------
    product_id: str
        The product ID
    nickname: str
        The user nickname

    Returns
    -------
    Dict[str, str | dict[str, str]]
        The reviews
    """
    logger.info("Getting reviews for %s", nickname)
    params = {"product_id": product_id, "user_name": nickname}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/reviews/", params=params)
        reviews = response.json()
        return reviews


async def post_review(product_id: str, nickname: str, review: str, rating: str) -> requests.Response:
    """
    Post reviews.

    Parameters
    ----------
    product_id: str
        The product ID
    nickname: str
        The nickname
    review: str
        The review
    rating: str
        The rating

    Returns
    -------
    requests.Response
        The response
    """
    logger.info("Posting review for %s", nickname)
    payload = {
        "product_id": product_id,
        "nickname": nickname,
        "review": review,
        "rating": len(rating),
        "timestamp": datetime.now().isoformat(),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}/reviews/", json=payload)
        return response


async def delete_review(mongo_id: str, product_id: str, nickname: str) -> requests.Response:
    """Delete reviews.

    Parameters
    ----------
    mongo_id: str
        The MongoDB ID
    product_id: str
        The product ID
    nickname: str
        The nickname

    Returns
    -------
    requests.Response
        The response
    """
    logger.info("Deleting review for %s", nickname)
    params = {"mongo_id": str(mongo_id), "product_id": product_id, "nickname": nickname}
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{BACKEND_URL}/reviews/", params=params)
        return r
