from pinecone import Pinecone

from backend.constants import PINECONE_INDEX_NAME


def test_pinecone_connection(pinecone_connection: Pinecone):
    """
    Test the Pinecone connection.

    Parameters
    ----------
    pinecone_connection: Pinecone
        Pinecone connection object
    """
    assert PINECONE_INDEX_NAME in [index.name for index in pinecone_connection.list_indexes()]


def test_pinecone_index(pinecone_connection: Pinecone):
    """
    Test the Pinecone index.

    Parameters
    ----------
    pinecone_connection: Pinecone
        Pinecone connection object
    """
    index = pinecone_connection.Index(PINECONE_INDEX_NAME)
    desc = index.describe_index_stats()

    assert desc["dimension"] == 384
    assert desc["total_vector_count"] > 0
