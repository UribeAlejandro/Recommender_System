import streamlit as st
from pymongo import MongoClient
from pymongo.database import Database

from web.constants import DATABASE_URL


@st.cache_resource
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
