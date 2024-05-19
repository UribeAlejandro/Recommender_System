import logging
from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import CollectionInvalid

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


def create_collection_index(mongo_database: Database, collection_indexes: dict[str, list[dict[str, str]]]) -> None:
    """
    Create indexes for the collections.

    Parameters
    ----------
    mongo_database : Database
        The MongoDB database
    collection_indexes : Dict[str, List[Dict[str, str]]]
        The collection indexes
    """
    for collection_name, indexes in collection_indexes.items():
        try:
            collection = mongo_database.create_collection(collection_name, check_exists=True)
            logger.info("Created collection %s", collection_name)
        except CollectionInvalid:
            logger.exception("Collection already exists: %s", collection_name)
            collection = mongo_database.get_collection(collection_name)

        for index in indexes:
            logger.info("Created index %s for collection %s", index["keys"], collection_name)
            collection.create_index(**index)


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

    for cleaned_url in product_urls:
        if collection.find_one({"url": cleaned_url}):
            logger.exception("URL already exists in MongoDB:, %s", cleaned_url)

        collection.insert_one(
            {"url": cleaned_url, "parent_url": parent_url, "status": "pending", "timestamp": datetime.now()}
        )
