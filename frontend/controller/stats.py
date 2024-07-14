import logging

import requests

from frontend.constants import BACKEND_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_rating_charts() -> dict:
    """
    Get rating charts.

    Returns
    -------
    Dict
        The rating charts
    """
    logger.info("Getting rating charts")
    response = requests.get(f"{BACKEND_URL}/stats/")
    rating_charts = response.json()

    return rating_charts
