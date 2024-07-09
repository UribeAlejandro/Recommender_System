import logging

from langchain_community.embeddings import GPT4AllEmbeddings
from pinecone import Index, Pinecone, QueryResponse

from backend.constants import EMBEDDINGS_MODEL, PINECONE_API_KEY, PINECONE_INDEX_NAME

logger = logging.getLogger(__name__)


def get_pinecone_index() -> Index:
    """
    Get Pinecone index.

    Returns
    -------
    Index
        Pinecone index object
    """
    pinecone = Pinecone(api_key=PINECONE_API_KEY)
    index = pinecone.Index(PINECONE_INDEX_NAME)

    return index


def get_recommendations(search_term: str, top_k: int = 5) -> QueryResponse:
    """
    Get recommendations from Pinecone index.

    Parameters
    ----------
    search_term: str
        Search term
    top_k: int (default=5)
        Number of recommendations to return

    Returns
    -------
    QueryResponse
        Recommendations
    """
    pinecone_index = get_pinecone_index()
    embed = get_embeddings(search_term)
    res = pinecone_index.query(vector=embed, top_k=top_k, include_metadata=True)
    return res


def get_embeddings(text: str) -> list[float]:
    """
    Get embeddings for the text.

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
    gpt4all_embd = GPT4AllEmbeddings(model_name=EMBEDDINGS_MODEL, gpt4all_kwargs=gpt4all_kwargs, verbose=True)
    return gpt4all_embd.embed_query(text)
