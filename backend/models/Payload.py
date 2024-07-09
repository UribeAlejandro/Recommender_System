from pydantic import BaseModel, Field


class ReviewPayload(BaseModel):
    """
    Review payload.

    Attributes
    ----------
    rating : int
        The rating
    nickname : str
        The nickname
    product_id : str
        The product ID
    review : str
        The review
    """

    rating: int
    nickname: str
    product_id: str
    review: str | None = Field(default=None)
