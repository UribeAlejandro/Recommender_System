from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database

from backend.constants import COLLECTION_DETAILS, DATABASE_NAME, DATABASE_URL


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


@lru_cache
def get_all_applicable_pets() -> list:
    """
    Get all applicable pets.

    Returns
    -------
    list
        The list of applicable pets
    """
    db = get_mongo_database(DATABASE_NAME)
    collection = db.get_collection(COLLECTION_DETAILS)
    all_applicable_pets_list = collection.distinct("description_items.applicable pet")
    return all_applicable_pets_list
