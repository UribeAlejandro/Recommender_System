import time
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter

from backend.constants import COLLECTION_REVIEWS, DATABASE_NAME
from backend.models.Collections import ProductReview
from backend.models.Payload import ReviewPayload
from backend.models.Response import ProductReviews
from backend.routes.utils import get_mongo_database

router = APIRouter()


@router.get("/reviews", status_code=200)
async def get_reviews(mongo_id: str, product_id: str, user_name: str):
    """
    Get reviews.

    Returns
    -------
    dict
        The reviews
    """
    db = get_mongo_database(DATABASE_NAME)
    collection_reviews = db.get_collection(COLLECTION_REVIEWS)
    already_reviewed = collection_reviews.find_one({"product_id": product_id, "nickname": user_name})
    mean_rating = collection_reviews.aggregate(
        [
            {"$match": {"product_id": product_id}},
            {"$group": {"_id": ObjectId(mongo_id), "mean": {"$avg": "$rating"}}},
            {"$project": {"_id": 0, "mean": 1}},
        ]
    )
    mean_rating = next(mean_rating, {"mean": 0})
    reviews = collection_reviews.find(
        {"product_id": product_id},
        {"_id": 0, "nickname": 1, "rating": 1, "review": 1, "date": 1, "product_id": 1, "timestamp": 1},
    ).sort({"timestamp": -1})
    reviews = ProductReviews(reviews=list(reviews)).reviews
    already_reviewed = ProductReview(**already_reviewed) if already_reviewed else None
    return {"already_reviewed": already_reviewed, "mean_rating": mean_rating, "reviews": reviews}


@router.post("/reviews", status_code=201)
async def post_reviews(payload: ReviewPayload):
    """
    Post reviews.

    Returns
    -------
    dict
        The reviews
    """
    db = get_mongo_database(DATABASE_NAME)
    collection_reviews = db.get_collection(COLLECTION_REVIEWS)
    collection_reviews.insert_one(
        {
            "product_id": payload.product_id,
            "nickname": payload.nickname,
            "rating": payload.rating,
            "review": payload.review,
            "date": time.strftime("%d %b, %Y"),
            "timestamp": datetime.now(),
        }
    )
    return {"status": "success"}
