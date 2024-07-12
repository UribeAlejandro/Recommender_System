import time
from datetime import datetime
from typing import Generic, TypeVar

from beanie import Document
from pydantic import Field

from backend.constants import COLLECTION_DETAILS, COLLECTION_REVIEWS

T = TypeVar("T")


class ProductDetails(Document):
    """
    Product details.

    Attributes
    ----------
    url : str
        The product URL
    title : str
        The product title
    image_path : str
        The product image path
    image_url : str
        The product image URL
    last_update : datetime
        The product last update
    product_id : str
        The product ID
    description_items : dict
        The product description items
    price : str
        The product price
    price_real : float
        The product real price
    price_discount : float
        The product discount price
    off_percent : int
        The product discount percent
    categories : List[str]
        The product categories
    main_category : str
        The product main category
    category : str
        The product category
    subcategory : str
        The product subcategory
    """

    url: str
    title: str
    image_path: str
    image_url: str
    last_update: datetime = Field(default_factory=datetime.now)
    product_id: str
    description_items: dict
    price: str | None
    price_real: float | None
    price_discount: float | None
    off_percent: int | None

    categories: list[str]
    main_category: str
    category: str
    subcategory: str

    class Settings:
        """
        Settings.

        Attributes
        ----------
        name : str
            The collection name
        max_nesting_depths_per_field : dict
            The max nesting depths per field
        """

        name = COLLECTION_DETAILS
        max_nesting_depths_per_field = {"description_items": 1}
        use_cache = True
        cache_capacity = 5


class ProductReview(Document):
    """
    Product review.

    Attributes
    ----------
    product_id : str
        The review product ID
    date : str
        The review date
    nickname : str
        The review nickname
    rating : int
        The review rating
    review : str
        The review
    timestamp : datetime
        The review timestamp
    """

    product_id: str
    date: str | None = Field(default=time.strftime("%d %b, %Y"))
    nickname: str | None = Field(default=None)
    rating: int | None = Field(default=0)
    review: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.now().isoformat)

    class Settings:
        """
        Settings.

        Attributes
        ----------
        name : str
            The collection name
        """

        name = COLLECTION_REVIEWS


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
