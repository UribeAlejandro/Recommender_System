import logging

import httpx

from frontend.constants import BACKEND_URL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def get_recommendations(nickname: str) -> list[dict]:
    """
    Get recommendations.

    Parameters
    ----------
    nickname: str
        The nickname

    Returns
    -------
    List[dict]
        The recommendations
    """
    logger.info("Getting recommendations for %s", nickname)
    params = {"nickname": nickname}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/recommender/", params=params, timeout=60)
        recommendations = response.json()
        return recommendations


# @cached(cache=Cache.MEMORY)
async def get_similar_products(mongo_id: str) -> list[dict]:
    """
    Get similar products.

    Parameters
    ----------
    mongo_id: str
        The product MongoDB ID

    Returns
    -------
    List[dict]
        The similar products
    """
    logger.info("Getting similar products for %s", mongo_id)
    params = {"mongo_id": mongo_id}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/recommender/similar", params=params)
        similar_products = response.json()
        return similar_products
