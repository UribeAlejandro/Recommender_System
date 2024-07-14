import logging

from pymongo import MongoClient

from recommender.constants import MONGO_URI
from recommender.products.collaborative import build_collaborative_filter
from recommender.products.content import build_similar_products

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Building recommenders")

    logger.info("Connecting to MongoDB")
    connection = MongoClient(MONGO_URI)

    logger.info("Building similar products' recommender")
    build_similar_products()

    logger.info("Building collaborative filtering recommender")
    build_collaborative_filter(connection)

    connection.close()
