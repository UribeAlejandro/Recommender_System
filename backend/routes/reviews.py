import logging

from beanie.operators import And, Eq
from bson import ObjectId
from fastapi import APIRouter
from pymongo import ASCENDING

from backend.models.Collections import ProductReview
from backend.models.Payload import ReviewPayload
from backend.models.Response import ProductReviews

router = APIRouter(prefix="/reviews", redirect_slashes=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


@router.get("/", status_code=200, response_model=ProductReviews)
async def get_reviews(product_id: str, user_name: str) -> ProductReviews:
    """
    Get reviews.

    Parameters
    ----------
    product_id: str
        The product ID
    user_name: str
        The username

    Returns
    -------
    ProductReviews
        The reviews
    """
    logger.info("Getting reviews...")
    already_reviewed = await ProductReview.find(
        And(Eq(ProductReview.product_id, product_id), Eq(ProductReview.nickname, user_name))
    ).to_list()
    mean_rating = await ProductReview.find(ProductReview.product_id == product_id).avg(ProductReview.rating)

    reviews = await (
        ProductReview.find(
            And(
                Eq(ProductReview.product_id, product_id),
            )
        )
        .sort([(ProductReview.timestamp, ASCENDING)])
        .to_list()
    )

    already_reviewed = already_reviewed if already_reviewed else None
    mean_rating = mean_rating if mean_rating else 0.0
    response_dict = {"already_reviewed": already_reviewed, "mean_rating": mean_rating, "reviews": reviews}
    response = ProductReviews(**response_dict)
    return response


@router.post("/", status_code=201)
async def post_review(payload: ReviewPayload):
    """
    Post reviews.

    Returns
    -------
    dict
        The reviews
    """
    logger.info("Posting review...")
    await ProductReview(**payload.model_dump()).insert()

    return {"status": "success"}


@router.delete("/", status_code=200)
async def delete_review(mongo_id: str, product_id: str, nickname: str) -> dict:
    """
    Delete review.

    Parameters
    ----------
    mongo_id: str
        The mongo ID of the review
    product_id: str
        The product ID
    nickname: str
        The nickname

    Returns
    -------
    dict
        The status
    """
    logger.info("Deleting review...")
    try:
        await (
            ProductReview.find(ProductReview.id == ObjectId(mongo_id))
            .find(
                And(
                    Eq(ProductReview.id, ObjectId(mongo_id)),
                    Eq(ProductReview.product_id, product_id),
                    Eq(ProductReview.nickname, nickname),
                )
            )
            .delete()
        )
        return {"status": "success"}
    except Exception:
        return {"status": "failed"}
