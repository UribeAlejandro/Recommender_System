import pandas as pd
from pymongo import MongoClient
from transformers import pipeline

from recommender.constants import MONGO_DATABASE, SENTIMENT_MODEL


def sentiment_analysis(connection: MongoClient) -> pd.DataFrame:
    """
    Perform sentiment analysis on product reviews.

    Parameters
    ----------
    connection: MongoClient
        The MongoDB connection

    Returns
    -------
    pd.DataFrame
        The data with sentiment analysis
    """
    data = extract(connection)
    data = transform(data)
    load(connection, data)
    return data


def extract(connection: MongoClient) -> pd.DataFrame:
    """
    Extract data from MongoDB.

    Parameters
    ----------
    connection: MongoClient
        The MongoDB connection

    Returns
    -------
    pd.DataFrame
        The data
    """
    db = connection[MONGO_DATABASE]
    input_data = db["product_reviews"]
    data = pd.DataFrame(list(input_data.find()))
    data = data.rename(columns={"review": "review_old"})
    return data


def transform(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the data.

    Parameters
    ----------
    data: pd.DataFrame
        The data

    Returns
    -------
    pd.DataFrame
        The transformed data

    """
    sentiment_pipeline = pipeline(
        task="sentiment-analysis",
        model=SENTIMENT_MODEL,
        tokenizer=SENTIMENT_MODEL,
        device="mps",
        batch_size=8,
        truncation=True,
    )
    sentiments = sentiment_pipeline(data["review_old"].to_list())
    data["review"] = [int(r["label"][0:1]) for r in sentiments]

    return data


def load(connection: MongoClient, data: pd.DataFrame) -> None:
    """
    Load the data to MongoDB.

    Parameters
    ----------
    connection: MongoClient
        The MongoDB connection
    data: pd.DataFrame
        The data to load
    """
    db = connection[MONGO_DATABASE]
    db["product_reviews"].drop()
    db["product_reviews"].insert_many(data.to_dict("records"))
