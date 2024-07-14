import logging

import requests

from frontend.constants import BACKEND_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user_reviews(nickname: str) -> list[dict]:
    """
    Get user reviews.

    Parameters
    ----------
    nickname: str
        The nickname

    Returns
    -------
    List[dict]
        The reviews
    """
    logger.info("Getting reviews for %s", nickname)
    params = {"nickname": nickname}
    response = requests.get(f"{BACKEND_URL}/user/reviews/", params=params)
    reviews = response.json()
    return reviews
