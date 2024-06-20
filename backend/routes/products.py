import logging

import pymongo
from beanie.operators import NE, And, Exists, In, RegEx
from bson import ObjectId
from fastapi import APIRouter

from backend.models.Collections import ProductDetails, ProductsPaged
from backend.models.Response import ProductsResponse

router = APIRouter(prefix="/products")
logger = logging.getLogger("uvicorn")


@router.get("/", status_code=200, response_model=ProductsResponse)
async def get_products(
    search: str = "",
    sort: str = "",
    applicable_pet: str = "",
    category: str = "",
    subcategory: str = "",
    page_size: int = 20,
    page_start: int = 0,
) -> ProductsPaged:
    """
    Get products.

    Parameters
    ----------
    search : str
        The search string for the product title
    sort : str
        The sort field
    applicable_pet : str
        Filter by applicable pet
    category : str
        Filter by category
    subcategory : str
        Filter by subcategory
    page_size : int
        The page size
    page_start : int
        The page start

    Returns
    -------
    ProductsPaged
        The products paged
    """
    all_category = await ProductDetails.distinct("category")
    all_subcategory = await ProductDetails.distinct("subcategory")
    all_applicable_pets_list = await ProductDetails.distinct("description_items.applicable pet")

    sort_key = ProductDetails.id, pymongo.DESCENDING

    if sort == "Relevance":
        sort_key = ProductDetails.id, pymongo.ASCENDING
    elif sort == "Highest Discount":
        sort_key = ProductDetails.off_percent, pymongo.DESCENDING
    elif sort == "Alphabetical: A-Z":
        sort_key = ProductDetails.title, pymongo.ASCENDING
    elif sort == "Alphabetical: Z-A":
        sort_key = ProductDetails.title, pymongo.DESCENDING
    elif sort == "Price: Low to High":
        sort_key = ProductDetails.price_discount, pymongo.ASCENDING
    elif sort == "Price: High to Low":
        sort_key = ProductDetails.price_discount, pymongo.DESCENDING

    title_search = search if search else ""
    category = category.split(",") if category else all_category
    subcategory = subcategory.split(",") if subcategory else all_subcategory
    app_pet = applicable_pet.split(",") if applicable_pet else all_applicable_pets_list

    filter_dict = And(
        Exists(ProductDetails.image_path, True),
        NE(ProductDetails.image_path, "pending"),
        RegEx(ProductDetails.title, title_search, "i"),
        In(ProductDetails.description_items["applicable pet"], app_pet),
        In(ProductDetails.category, category),
        In(ProductDetails.subcategory, subcategory),
    )
    number = await ProductDetails.find(filter_dict).count()
    products_list = await ProductDetails.find(filter_dict, limit=page_size, skip=page_start).sort([sort_key]).to_list()

    return ProductsPaged(
        number, products_list, page_size + page_start < number, all_applicable_pets_list, all_category, all_subcategory
    )


@router.post("/details", status_code=200, response_model=ProductDetails)
async def get_product(filter_dict: dict) -> ProductDetails:
    """
    Get product.

    Parameters
    ----------
    filter_dict: dict
        The filter dictionary

    Returns
    -------
    ProductDetails
        The product
    """
    product_filter = {k: (ObjectId(v) if k == "_id" else v) for k, v in filter_dict.items()}
    product = await ProductDetails.find_one(product_filter)
    return product
