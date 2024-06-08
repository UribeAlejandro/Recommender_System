import logging

from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from backend.constants import COLLECTION_DETAILS, DATABASE_NAME
from backend.models.Collections import ProductDetails
from backend.models.Response import ProductsResponse
from backend.routes.utils import get_all_applicable_pets, get_mongo_database

router = APIRouter(prefix="/products")
logger = logging.getLogger("uvicorn")


@router.get("/", status_code=200, response_class=ORJSONResponse, response_model=ProductsResponse)
async def get_products(search: str, applicable_pet: str):
    """
    Get products.

    Returns
    -------
    dict
        The products
    """
    logger.info("Getting products...")
    all_applicable_pets_list = get_all_applicable_pets()

    db = get_mongo_database(DATABASE_NAME)
    collection = db.get_collection(COLLECTION_DETAILS)
    title_search = search if search else ""
    app_pet = applicable_pet.split(",") if applicable_pet else all_applicable_pets_list

    filter_dict = {
        "$and": [
            {"image_path": {"$exists": True}},
            {"image_path": {"$ne": "pending"}},
            {"title": {"$regex": title_search, "$options": "i"}},
            {"description_items.applicable pet": {"$in": app_pet}},
        ]
    }

    products = collection.find(
        filter_dict,
        {
            "_id": 1,
            "title": 1,
            "image_path": 1,
            "product_id": 1,
            "price_discount": 1,
            "off_percent": 1,
            "description_items.applicable pet": 1,
        },
    )
    response = ProductsResponse(products=list(products))
    return ORJSONResponse(response.model_dump())


@router.post("/details", status_code=200)
async def get_product(product_filter: dict):
    """
    Get product.

    Returns
    -------
    dict
        The product
    """
    db = get_mongo_database(DATABASE_NAME)
    collection_products = db.get_collection(COLLECTION_DETAILS)
    product_filter = {k: (ObjectId(v) if k == "_id" else v) for k, v in product_filter.items()}

    product_details = collection_products.find_one(
        product_filter,
        {
            "_id": 1,
            "title": 1,
            "image_path": 1,
            "product_id": 1,
            "price_discount": 1,
            "price_real": 1,
            "off_percent": 1,
            "description_items": 1,
        },
    )
    return ProductDetails(**product_details)
