import logging

from beanie.operators import In
from fastapi import APIRouter

from backend.models.Collections import ProductDetails, ProductReview

router = APIRouter(prefix="/recommender")
logger = logging.getLogger("uvicorn")


@router.get("/", status_code=200, response_model=None)
async def get_recommendations(nickname: str):
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
