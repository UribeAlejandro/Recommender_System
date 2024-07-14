import logging

import pandas as pd
from pymongo import MongoClient

from recommender.constants import MONGO_DATABASE, MONGO_URI

logger = logging.getLogger(__name__)


def extract_data(collection_name: str) -> pd.DataFrame:
    """
    Get products data from MongoDB.

    Parameters
    ----------
    collection_name : str
        The collection name

    Returns
    -------
    pd.DataFrame
        The products data
    """
    logger.info("Getting Product Details data from MongoDB")

    connection = MongoClient(MONGO_URI)
    db = connection[MONGO_DATABASE]

    input_data = db[collection_name]
    data = pd.DataFrame(list(input_data.find()))

    connection.close()
    return data


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the data.

    Parameters
    ----------
    data : pd.DataFrame
        The data

    Returns
    -------
    pd.DataFrame
        The transformed data
    """
    logger.info("Transforming the data")

    data["full_description"] = data.apply(couple, axis=1)
    return data


def load_data(data: pd.DataFrame, path_out: str) -> None:
    """
    Load the data to CSV.

    Parameters
    ----------
    data : pd.DataFrame
        The data
    path_out : str
        The output path
    """
    logger.info("Loading the data to MongoDB")
    data.to_csv(path_out, index=False)


def couple(x: pd.Series) -> str:
    """
    Couple the title, category, subcategory, and description.

    Parameters
    ----------
    x: pd.Series
        The row of the DataFrame

    Returns
    -------
    str
        The coupled text
    """
    return f"{x['title']} {x['main_category']} {x['category']} {x['subcategory']}"
