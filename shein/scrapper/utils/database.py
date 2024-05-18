import logging
from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database

from shein.constants import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_mongo_database(database_name: str) -> Database:
    """
    Set up the MongoDB client.

    Parameters
    ----------
    database_name : str
        The database name

    Returns
    -------
    Database
        The MongoDB database
    """
    mongo_client = MongoClient(DATABASE_URL)
    mongo_database = mongo_client[database_name]

    return mongo_database


def write_in_database(parent_url: str, product_urls: list[str], mongo_database: Database, collection_name: str) -> None:
    """
    Write the product URLs in MongoDB.

    Parameters
    ----------
    parent_url : str
        The parent URL
    product_urls : List[str]
        The product URLs
    mongo_database : Database
        The MongoDB database
    collection_name : str
        The collection name
    """
    collection = mongo_database[collection_name]

    try:
        collection.create_index("url", unique=True)
        logger.info("Index created")
    except Exception as e:
        logger.warning("Index already exists")
        logger.exception(e)

    for cleaned_url in product_urls:
        if collection.find_one({"url": cleaned_url}):
            logger.exception("URL already exists in MongoDB:, %s", cleaned_url)

        collection.insert_one(
            {"url": cleaned_url, "parent_url": parent_url, "status": "pending", "timestamp": datetime.now()}
        )
