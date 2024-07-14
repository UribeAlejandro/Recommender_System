import logging

from beanie.odm.operators.find.logical import Not
from beanie.operators import In
from bson import ObjectId
from fastapi import APIRouter

from backend.models.Collections import ProductDetails, ProductReview
from backend.utils.recommender import collaborative_filtering, get_recommendations, main_forty_products

router = APIRouter(prefix="/recommender", redirect_slashes=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


@router.get("/", status_code=200, response_model=None)
async def user_recommendations(nickname: str):
    """
    Get user recommendations.

    Parameters
    ----------
    nickname : str
        The nickname

    Returns
    -------
    dict
        The user recommendations
    """
    logger.info("Getting recommendations for %s", nickname)
    number_of_reviews = await ProductReview.find(ProductReview.nickname == nickname).count()
    seen_products = await ProductReview.find(ProductReview.nickname == nickname).to_list()
    seen_products_ids = [product.product_id for product in seen_products]

    if number_of_reviews < 11:
        model = "40 principales"
        logger.info("%s", model)
        items, number = await main_forty_products(seen_products_ids)
    else:
        model = "Collaborative filtering"
        logger.info("%s", model)
        logger.info("User %s has %s reviews", nickname, number_of_reviews)

        items, number = await collaborative_filtering(seen_products_ids, nickname)

    return {"items": items, "number": number, "model": model}


@router.get("/similar", status_code=200, response_model=None)
async def get_similar_products(mongo_id: str) -> list[ProductDetails]:
    """
    Get similar products.

    Parameters
    ----------
    mongo_id : str
        The product MongoDB ID

    Returns
    -------
    list[ProductDetails]
        The similar products
    """
    mongo_id = ObjectId(mongo_id)

    product = await ProductDetails.get(mongo_id)

    product = product.model_dump()
    search_term = f"{product['title']} {product['main_category']} {product['category']} {product['subcategory']}"

    res = get_recommendations(search_term, str(mongo_id), 5)
    mongo_ids = [ObjectId(r.metadata["_id"]) for r in res.matches]

    products = await ProductDetails.find(Not(ProductDetails.id == mongo_id), In(ProductDetails.id, mongo_ids)).to_list()
    return products
