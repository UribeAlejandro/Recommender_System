import mlflow
import pandas as pd
from pymongo import MongoClient

from recommender.constants import MLFLOW_EXPERIMENT_NAME, MLFLOW_REGISTRY_URI, MONGO_DATABASE
from recommender.utils.sentiment import sentiment_analysis


def build_collaborative_filter(connection: MongoClient) -> None:
    """Build collaborative filtering recommender."""
    data = preprocess(connection)
    predictions = collaborative_filter(data, connection)
    load_to_collection(predictions, connection)


def preprocess(connection: MongoClient) -> pd.DataFrame:
    """Preprocess data."""
    data = sentiment_analysis(connection)
    data = data[["nickname", "product_id", "rating"]]
    data = data.rename(columns={"nickname": "userID", "product_id": "itemID", "rating": "rating"})
    return data


def collaborative_filter(data: pd.DataFrame, connection: MongoClient) -> pd.DataFrame:
    """
    Build similar products' recommender.

    Parameters
    ----------
    data : pd.DataFrame
        The data to build the recommender
    connection : MongoClient
        The MongoDB connection

    Returns
    -------
    pd.DataFrame
        The data with the recommender
    """
    mlflow.set_registry_uri(MLFLOW_REGISTRY_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    # TODO: Implement the collaborative filtering algorithm

    return data


def load_to_collection(data: pd.DataFrame, connection: MongoClient, collection_name: str, drop: bool = False) -> None:
    """
    Load recommendations to MongoDB.

    Parameters
    ----------
    data : pd.DataFrame
        The data to load
    connection : MongoClient
        The MongoDB connection
    collection_name : str
        The collection name
    drop : bool (default=False)
        Whether to drop the collection
    """
    db = connection[MONGO_DATABASE]
    if drop:
        db[collection_name].drop()

    db[collection_name].insert_many(data.to_dict(orient="records"))
