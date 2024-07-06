import logging

import pandas as pd
from pymongo import MongoClient

from recommender.constants import MONGO_DATABASE, MONGO_URI

logger = logging.getLogger(__name__)


def get_products_data():
    """Get products data from MongoDB and save it to a CSV file."""
    connection = MongoClient(MONGO_URI)
    db = connection[MONGO_DATABASE]
    input_data = db["product_details"]
    data = pd.DataFrame(list(input_data.find()))
    data.to_csv("data/raw/shein-mirror.csv", index=False)
    connection.close()
