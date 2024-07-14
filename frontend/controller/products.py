import logging

import httpx

from frontend.constants import BACKEND_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_products(
    search: str, sort: str, app_pet: list[str], category: list[str], subcategory: list[str], page_size: int, page: int
) -> dict[str, str]:
    """
    Get products.

    Parameters
    ----------
    search: str
        The search string for the product title
    sort: str
        The sort field
    app_pet: list[str]
        Filter by applicable pet
    category: list[str]
        Filter by category
    subcategory: list[str]
        Filter by subcategory
    page_size: int
        The page size
    page: int
        The page

    Returns
    -------
    List[dict]
        The products
    """
    logger.info("Getting products")

    page_start = (page - 1) * page_size
    params = {
        "search": search,
        "sort": sort,
        "applicable_pet": ",".join(app_pet),
        "category": ",".join(category),
        "subcategory": ",".join(subcategory),
        "page_size": page_size,
        "page_start": page_start,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/products/", params=params)
        return response.json()


async def get_product(filter_dict: dict) -> dict[str, str]:
    """
    Get product.

    Parameters
    ----------
    filter_dict: dict
        The filter dictionary

    Returns
    -------
    Dict[str, str]
        The product
    """
    logger.info("Getting product")

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}/products/details", json=filter_dict)
        product_details = response.json()
        return product_details
