import logging
from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import CollectionInvalid

from shein.constants import COLLECTION_DETAILS, DATABASE_URL

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


def write_url_in_database(
    parent_url: str, product_urls: list[str], mongo_database: Database, collection_name: str
) -> None:
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


def clean_price_column(mongo_database: Database):
    """
    Clean the columns in the MongoDB database.

    Parameters
    ----------
    mongo_database : Database
        The MongoDB database
    """
    collection_details = mongo_database[COLLECTION_DETAILS]
    pipeline = [
        {"$addFields": {"price_clean": {"$replaceAll": {"input": "$price", "find": "From", "replacement": ""}}}},
        {
            "$set": {
                "price_clean": {"$replaceAll": {"input": "$price_clean", "find": {"$literal": "$"}, "replacement": ""}}
            }
        },
        {
            "$set": {
                "price_clean": {
                    "$trim": {
                        "input": "$price_clean",
                    }
                }
            }
        },
        {"$set": {"price_clean": {"$split": ["$price_clean", "\n"]}}},
        {
            "$addFields": {
                "price_discount": {"$arrayElemAt": ["$price_clean", 0]},
                "price_real": {"$arrayElemAt": ["$price_clean", 1]},
                "off_percent": {"$arrayElemAt": ["$price_clean", 2]},
            }
        },
        {
            "$set": {
                "off_percent": {"$replaceAll": {"input": "$off_percent", "find": {"$literal": "%"}, "replacement": ""}}
            }
        },
        {"$unset": "price"},
        {"$unset": "price_clean"},
        {
            "$set": {
                "off_percent": {"$toInt": "$off_percent"},
                "price_real": {"$toDouble": "$price_real"},
                "price_discount": {"$toDouble": "$price_discount"},
            }
        },
    ]
    collection_details.update_many({}, pipeline)


def get_categories(mongo_database: Database):
    """
    Get the categories for the products.

    Parameters
    ----------
    mongo_database: Database
        The MongoDB database

    Returns
    -------
    None
    """
    collection_details = mongo_database[COLLECTION_DETAILS]
    pipeline = [
        {
            "$addFields": {
                "main_category": {"$arrayElemAt": ["$categories", 0]},
                "category": {"$arrayElemAt": ["$categories", 1]},
                "subcategory": {"$arrayElemAt": ["$categories", 2]},
            }
        }
    ]
    collection_details.update_many({}, pipeline)
