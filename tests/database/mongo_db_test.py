from pymongo import MongoClient


def test_mongo_db_connection(mongo_connection: MongoClient):
    """
    Test the MongoDB connection.

    Parameters
    ----------
    mongo_connection: MongoClient
        The MongoDB connection
    """
    assert mongo_connection.server_info()
