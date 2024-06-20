from pydantic import BaseModel, Field

from backend.models.Collections import ProductDetails, ProductReview


class ProductsResponse(BaseModel):
    """
    Products response.

    Attributes
    ----------
    number : int
        The number of products
    items : list[ProductDetails]
        The products
    more_pages : bool
        The more pages flag
    applicable_pets : list[str]
        The applicable pets list
    categories : list[str]
        The categories list
    subcategories : list[str]
        The subcategories list
    """

    number: int = Field(default=0)
    items: list[ProductDetails] | None = Field(default=None)
    more_pages: bool = Field(default=False)
    applicable_pets: list[str] | None = Field(default=None)
    categories: list[str] | None = Field(default=None)
    subcategories: list[str] | None = Field(default=None)


class ProductReviews(BaseModel):
    """
    Product reviews.

    Attributes
    ----------
    reviews : list[ProductReview]
        The reviews
    """

    already_reviewed: list[ProductReview] | None = Field(default=None)
    reviews: list[ProductReview] | None = Field(default=None)
    mean_rating: float = Field(default=0.0)
