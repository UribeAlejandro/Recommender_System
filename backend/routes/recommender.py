import logging

from beanie.odm.operators.find.logical import Not
from beanie.operators import In
from bson import ObjectId
from fastapi import APIRouter

from backend.models.Collections import ProductDetails, ProductReview
from backend.recommender.utils import get_recommendations

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

    user_s_most_reviews = await ProductReview.aggregate(
        [{"$sortByCount": "$nickname"}, {"$project": {"_id": 1, "count": 1}}, {"$limit": 15}]
    ).to_list()
    print(user_s_most_reviews)

    if number_of_reviews <= 5:
        model = "40 principales"
        pipeline = [
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

    else:
        items = []
        model = "No model"

    number = await result.count()
    return {"items": items, "number": number, "model": model}


@router.get("/similar", status_code=200, response_model=None)
async def get_similar_products(title: str) -> list[ProductDetails]:
    """
    Get similar products.

    Parameters
    ----------
    title : str
        The title

    Returns
    -------
    list[ProductDetails]
        The similar products
    """
    res = get_recommendations(title, 7)
    mongo_ids = [ObjectId(r.metadata["_id"]) for r in res.matches]
    products = await ProductDetails.find(In(ProductDetails.id, mongo_ids), Not(ProductDetails.title == title)).to_list()
    products = products[:5]

    return products
