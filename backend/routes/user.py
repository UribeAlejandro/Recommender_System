from fastapi import APIRouter

from backend.constants import COLLECTION_REVIEWS, DATABASE_NAME
from backend.models.Response import ProductReviews
from backend.routes.utils import get_mongo_database

router = APIRouter(prefix="/user")


@router.get("/reviews", status_code=200)
async def get_reviews(nickname: str):
    """
    Get reviews.

    Returns
    -------
    dict
        The reviews
    """
    db = get_mongo_database(DATABASE_NAME)
    collection_reviews = db.get_collection(COLLECTION_REVIEWS)

    reviews = list(collection_reviews.find({"nickname": nickname}).sort({"timestamp": -1}))
    reviews = ProductReviews(reviews=list(reviews)).reviews

    return reviews
