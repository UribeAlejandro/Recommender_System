import logging

import pandas as pd
from langchain_community.embeddings import GPT4AllEmbeddings
from pinecone import Index, Pinecone, QueryResponse, ServerlessSpec

from recommender.constants import CHUNK_SIZE, EMBEDDINGS_MODEL, PINECONE_API_KEY, PINECONE_INDEX_NAME, TOTAL_ROWS

logger = logging.getLogger(__name__)


def get_embeddings(text: str) -> list[float]:
    """
    Get embeddings for the text

    Parameters
    ----------
    text: str
        Text to embed

    Returns
    -------
    list[float]
        Embeddings
    """
    gpt4all_kwargs = {"allow_download": "True"}
    gpt4all_embd = GPT4AllEmbeddings(model_name=EMBEDDINGS_MODEL, gpt4all_kwargs=gpt4all_kwargs)
    return gpt4all_embd.embed_query(text)


def get_recommendations(pinecone_index: Index, search_term: str, top_k: int = 10) -> QueryResponse:
    """
    Get recommendations from Pinecone index

    Parameters
    ----------
    pinecone_index: Index
        Pinecone index object
    search_term: str
        Search term
    top_k: int (default=10)
        Number of recommendations to return

    Returns
    -------
    dict
        Recommendations
    """
    embed = get_embeddings(search_term)
    res = pinecone_index.query(vector=embed, top_k=top_k, include_metadata=True)
    return res


def get_or_create_pinecone_index() -> Index:
    """
    Get or create Pinecone index

    Returns
    -------
    Index
        Pinecone index object
    """
    logger.info("Creating Pinecone index %s", PINECONE_INDEX_NAME)
    pinecone = Pinecone(api_key=PINECONE_API_KEY)
    if PINECONE_INDEX_NAME in [index.name for index in pinecone.list_indexes()]:
        pinecone.delete_index(PINECONE_INDEX_NAME)

    pinecone.create_index(
        name=PINECONE_INDEX_NAME, dimension=384, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)

    logger.info("Created Pinecone index %s", PINECONE_INDEX_NAME)
    logger.info("Index details: %s", index.describe_index_stats())

    return index


def embed_data_to_pinecone(index: Index) -> None:
    """
    Embed data to Pinecone index

    Parameters
    ----------
    index: Index
        Pinecone index object
    """
    chunks = pd.read_csv("data/raw/shein-mirror.csv", chunksize=CHUNK_SIZE, nrows=TOTAL_ROWS)
    chunk_num = 0
    for chunk in chunks:
        titles = chunk["title"].tolist()
        _ids = chunk["_id"].tolist()
        prepped = [
            {
                "id": str(chunk_num * CHUNK_SIZE + i),
                "values": get_embeddings(titles[i]),
                "metadata": {"title": titles[i], "_id": str(_ids[i])},
            }
            for i in range(0, len(titles))
        ]
        chunk_num = chunk_num + 1
        if len(prepped) >= 200:
            index.upsert(prepped)
            prepped = []

    logger.info("Finished embedding data to Pinecone")
    logger.info("Index details: %s", index.describe_index_stats())
