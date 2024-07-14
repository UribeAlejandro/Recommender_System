from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from backend.models.Collections import ProductDetails, ProductReview

T = TypeVar("T")


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


class ProductsPaged(Generic[T]):
    """
    Paged.

    Attributes
    ----------
    items : List[T]
        The items list
    size : int
        The size of the items list
    more_pages : bool
        The more pages flag
    applicable_pets : List[str]
        The applicable pets list
    categories : List[str]
        The categories list
    subcategories : List[str]
        The subcategories list
    """

    items: list[T]
    size: int
    more_pages: bool
    applicable_pets: list[str]
    categories: list[str]
    subcategories: list[str]

    def __init__(
        self,
        number: int,
        items: list[T],
        more_pages: bool,
        applicable_pets: list[str],
        categories: list[str],
        subcategories: list[str],
    ):
        """
        Initialize the Paged.

        Parameters
        ----------
        number: int
            The number of products
        items: List[T]
            The products list
        more_pages: bool
            The more pages flag
        applicable_pets: List[str]
            The applicable pets list
        categories: List[str]
            The categories list
        subcategories: List[str]
            The subcategories list
        """
        self.items = items
        self.number = number
        self.more_pages = more_pages
        self.applicable_pets = applicable_pets
        self.categories = categories
        self.subcategories = subcategories
