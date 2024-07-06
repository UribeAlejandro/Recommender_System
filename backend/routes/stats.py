import logging

import pandas as pd
import plotly.express as px
from fastapi import APIRouter
from pydantic import BaseModel

from backend.models.Collections import ProductDetails, ProductReview

router = APIRouter(prefix="/stats")
logger = logging.getLogger("uvicorn")


class Ratings(BaseModel):
    """Ratings model."""

    rating: int


@router.get("/", status_code=200, response_model=None)
async def get_stats():
    """
    Get stats.

    Returns
    -------
    dict
        Plots and stats
    """
    response = {}
    response["number_of_reviews"] = await ProductReview.count()
    response["number_of_products"] = await ProductDetails.count()
    distinct_of_users = await ProductReview.distinct("nickname")
    response["number_of_users"] = len(distinct_of_users)
    reviews = await ProductReview.find().to_list()
    reviews = [review.model_dump() for review in reviews]

    reviews = pd.DataFrame(reviews)

    fig = px.histogram(reviews, x="rating", color="rating", title="Rating Distribution", text_auto=True)
    response["rating_distribution"] = fig.to_json()

    fig = px.histogram(reviews, x="rating", y="price_real", color="rating", title="Rating Distribution", text_auto=True)
    response["rating_distribution_price"] = fig.to_json()

    return response
