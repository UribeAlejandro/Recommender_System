from pydantic import BaseModel, Field

from backend.models.Collections import ProductDetails, ProductReview


class ProductsResponse(BaseModel):
    """
    Products response.

    Attributes
    ----------
    products : list[ProductDetails]
        The products
    """

    products: list[ProductDetails] | None = Field(default=None)


class ProductReviews(BaseModel):
    """
    Product reviews.

    Attributes
    ----------
    reviews : list[ProductReview]
        The reviews
    """

    reviews: list[ProductReview] | None = Field(default=None)
