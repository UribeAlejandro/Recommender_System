import logging
from functools import lru_cache

import pandas as pd
from beanie.odm.operators.find.comparison import In
from langchain_community.embeddings import GPT4AllEmbeddings
from pinecone import Index, Pinecone, QueryResponse
from surprise import SVD, BaselineOnly, Dataset, Reader

from backend.constants import EMBEDDINGS_MODEL, PINECONE_API_KEY, PINECONE_INDEX_NAME
from backend.models import ProductDetails, ProductReview

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


@lru_cache
def get_pinecone_index() -> Index:
    """
    Get Pinecone index.

    Returns
    -------
    Index
        Pinecone index object
    """
    logger.info("Getting Pinecone index...")

    pinecone = Pinecone(api_key=PINECONE_API_KEY)
    index = pinecone.Index(PINECONE_INDEX_NAME)

    return index


def get_recommendations(search_term: str, mongo_id: str, top_k: int = 5) -> QueryResponse:
    """
    Get recommendations from Pinecone index.

    Parameters
    ----------
    search_term: str
        Search term
    mongo_id: str
        MongoDB ID
    top_k: int (default=5)
        Number of recommendations to return

    Returns
    -------
    QueryResponse
        Recommendations
    """
    logger.info("Getting recommendations...")

    filter_query = {"_id": {"$ne": mongo_id}}
    pinecone_index = get_pinecone_index()
    embed = get_embeddings(search_term)
    res = pinecone_index.query(vector=embed, filter=filter_query, top_k=top_k, include_metadata=True)
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
    logger.info("Getting embeddings...")

    gpt4all_kwargs = {"allow_download": "True"}
    gpt4all_embd = GPT4AllEmbeddings(model_name=EMBEDDINGS_MODEL, gpt4all_kwargs=gpt4all_kwargs, verbose=True)
    return gpt4all_embd.embed_query(text)


async def main_forty_products(seen_products_ids: list[str], max_items: int = 40) -> tuple[list[ProductDetails], int]:
    """
    Get the main 40 products.

    Parameters
    ----------
    seen_products_ids: list[str]
        Seen products IDs by the user
    max_items: int (default=40)
        Maximum number of items to return

    Returns
    -------
    tuple[list[ProductDetails], int]
        The items and the number of items
    """
    pipeline = [
        {"$match": {"product_id": {"$nin": seen_products_ids}}},
        {"$group": {"_id": "$product_id", "average_rating": {"$avg": "$rating"}, "review_count": {"$sum": 1}}},
        {"$sort": {"review_count": -1, "average_rating": -1}},
        {"$limit": max_items},
        {"$project": {"_id": 1}},
    ]

    products = await ProductReview.aggregate(pipeline).to_list()
    products_ids = [product["_id"] for product in products]

    result = ProductDetails.find(
        In(ProductDetails.product_id, products_ids),
    )
    items = await result.to_list()
    number = await result.count()

    return items, number


async def collaborative_filtering(
    seen_products_ids: list[str], nickname: str, max_items: int = 40
) -> tuple[list[ProductDetails], int]:
    """
    Collaborative filtering recommender system.

    Parameters
    ----------
    seen_products_ids: list[str]
        Seen products IDs by the user
    nickname: str
        The user nickname
    max_items: int (default=40)
        Maximum number of items to return

    Returns
    -------
    tuple[list[ProductDetails], int]
        The items and the number of items
    """
    reviews_pipeline = [{"$project": {"nickname": 1, "product_id": 1, "rating": 1}}]
    not_seen_prods_pipeline = [{"$match": {"product_id": {"$nin": seen_products_ids}}}, {"$project": {"product_id": 1}}]

    reviews = await ProductReview.aggregate(reviews_pipeline).to_list()
    not_seen = await ProductDetails.aggregate(not_seen_prods_pipeline).to_list()

    df = pd.DataFrame([review for review in reviews])
    not_seen = [product["product_id"] for product in not_seen]

    df = df[["nickname", "product_id", "rating"]]
    df = df.rename(columns={"nickname": "userID", "product_id": "itemID", "rating": "rating"})

    rating_min = df["rating"].min()
    rating_max = df["rating"].max()

    reader = Reader(rating_scale=(rating_min, rating_max))
    data = Dataset.load_from_df(df[["userID", "itemID", "rating"]], reader)

    trainset = data.build_full_trainset()
    algos = [BaselineOnly(), SVD()]
    all_recomendaciones = []

    for algo in algos:
        algo.fit(trainset)
        predicciones = []

        for not_seen_prod in not_seen:
            raw_predicciones = algo.predict(nickname, not_seen_prod, verbose=False)

            if not raw_predicciones.details["was_impossible"]:
                predicciones.append(raw_predicciones.est)

        rating_prod = [(p, not_seen_prod) for (p, not_seen_prod) in zip(predicciones, not_seen)]

        # Below you can find yet another try to filter the recommendations by rating
        # above_4 = [r for r in rating_prod if r[0] >= 4]
        # between_3_4 = [r for r in rating_prod if 3 <= r[0] < 4]
        # below_3 = [r for r in rating_prod if r[0] < 3]
        # all_recomendaciones.extend(above_4[:5])
        # all_recomendaciones.extend(between_3_4[:5])
        # all_recomendaciones.extend(below_3[:5])

        all_recomendaciones.extend(rating_prod)

    all_recomendaciones = list(set(sorted(all_recomendaciones, reverse=True)))

    result = ProductDetails.find(In(ProductDetails.product_id, [r[1] for r in all_recomendaciones]), limit=max_items)

    items = await result.to_list()
    number = await result.count()

    return items, number
