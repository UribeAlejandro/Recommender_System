import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pinecone import Pinecone
from pymongo import MongoClient

from backend.constants import MONGO_URI, PINECONE_API_KEY
from backend.main import create_application

load_dotenv()


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Yields
    ------
    TestClient
        The test client
    """
    client = TestClient(create_application())
    yield client


@pytest.fixture(scope="module")
def pinecone_connection() -> Pinecone:
    """
    Get Pinecone index.

    Returns
    -------
    Index
        Pinecone index object
    """
    pinecone = Pinecone(api_key=PINECONE_API_KEY)

    yield pinecone


@pytest.fixture(scope="module")
def mongo_connection() -> MongoClient:
    """
    Get Mongo connection.

    Returns
    -------
    Index
        Mongo connection object
    """
    client = MongoClient(MONGO_URI)
    # mongo = client[DATABASE_NAME]

    yield client

    client.close()
