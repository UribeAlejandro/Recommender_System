import logging

import pandas as pd
from pymongo import MongoClient

from recommender.constants import MONGO_DATABASE, MONGO_URI, PATH_PRODUCT_DETAILS

logger = logging.getLogger(__name__)


def get_products_details() -> None:
    """Get products data from MongoDB and save it to a CSV file."""
    logger.info("Getting Product Details data from MongoDB")

    connection = MongoClient(MONGO_URI)
    db = connection[MONGO_DATABASE]
    input_data = db["product_details"]
    data = pd.DataFrame(list(input_data.find()))
    data.to_csv(PATH_PRODUCT_DETAILS, index=False)
    connection.close()
