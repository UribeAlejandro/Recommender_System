import logging

from beanie.odm.operators.find.logical import Not
from beanie.operators import In
from bson import ObjectId
from fastapi import APIRouter

from backend.models.Collections import ProductDetails, ProductReview
from backend.utils.recommender import get_recommendations

router = APIRouter(prefix="/recommender")
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
    number_of_reviews = await ProductReview.find(ProductReview.nickname == nickname).count()

    # user_s_most_reviews = await ProductReview.aggregate(
    #     [{"$sortByCount": "$nickname"}, {"$project": {"_id": 1, "count": 1}}, {"$limit": 15}]
    # ).to_list()

    seen_products = await ProductReview.find(ProductReview.nickname == nickname).to_list()
    seen_products_ids = [product.product_id for product in seen_products]

    if number_of_reviews <= 5:
        model = "40 principales"
        pipeline = [
            {"$match": {"product_id": {"$nin": seen_products_ids}}},
            {"$group": {"_id": "$product_id", "average_rating": {"$avg": "$rating"}, "review_count": {"$sum": 1}}},
            {"$sort": {"review_count": -1, "average_rating": -1}},
            {"$limit": 40},
            {"$project": {"_id": 1}},
        ]

        products = await ProductReview.aggregate(pipeline).to_list()
        products_ids = [product["_id"] for product in products]

        result = ProductDetails.find(
            In(ProductDetails.product_id, products_ids),
        )
        items = await result.to_list()
        number = await result.count()

    else:
        items = []
        model = "No model"
        number = 0
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
