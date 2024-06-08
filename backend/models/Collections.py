import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProductDetails(BaseModel):
    """
    Product details.

    Attributes
    ----------
    id : PyObjectId
        The product ID
    url : str
        The product URL
    title : str
        The product title
    off_percent : str
        The product off percent
    price_real : str
        The product real price
    price_discount : str
        The product discount price
    image_url : str
        The product image URL
    product_id : str
        The product ID
    image_path : str
        The product image path
    last_update : str
        The product last update
    description_items : dict[str, str]
        The product description items
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: PyObjectId | None = Field(alias="_id")
    url: str | None = Field(default=None)
    title: str | None = Field(default=None)

    # price: Optional[str]
    off_percent: int | None = Field(default=None)
    price_real: float | None = Field(default=0)
    price_discount: float = Field(default=0)

    image_url: str | None = Field(default=None)
    product_id: str | None = Field(default=None)
    image_path: str | None = Field(default=None)
    last_update: str = Field(default=None)
    description_items: dict[str, str] | None = Field(default=None)


class ProductReview(BaseModel):
    """
    Product review.

    Attributes
    ----------
    id : PyObjectId
        The MongoDB ID
    date : str
        The review date
    nickname : str
        The review nickname
    product_id : str
        The review product ID
    rating : int
        The review rating
    review : str
        The review
    timestamp : datetime
        The review timestamp
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: PyObjectId | None = Field(alias="_id", default=None)
    date: str | None = Field(default=None)
    nickname: str | None = Field(default=None)
    product_id: str | None = Field(default=None)
    rating: int | None = Field(default=0)
    review: str | None = Field(default=None)
    timestamp: datetime = Field(default=None)


class ProductURL(BaseModel):
    """
    Product URL.

    Attributes
    ----------
    id : PyObjectId
        The MongoDB ID
    parent_url : str
        The parent URL
    status : str
        The URL status
    timestamp : str
        The URL timestamp
    url : str
        The URL
    """

    id: PyObjectId | None = Field(alias="_id", default=None)
    parent_url: str | None = Field(default=None)
    status: str | None = Field(default=None)
    timestamp: str | None = Field(default=None)
    url: str | None = Field(default=None)
