import requests
import streamlit as st
from pymongo import MongoClient
from pymongo.database import Database

from frontend.constants import DATABASE_URL


@st.cache_resource
def get_mongo_database(database_name: str) -> Database:
    """
    Set up the MongoDB client.

    Parameters
    ----------
    database_name : str
        The database name

    Returns
    -------
    Database
        The MongoDB database
    """
    mongo_client = MongoClient(DATABASE_URL)
    mongo_database = mongo_client[database_name]

    return mongo_database


@st.cache_resource
def get_all_applicable_pets() -> list[str]:
    """
    Get all applicable pets.

    Returns
    -------
    list
        The list of applicable pets
    """
    all_applicable_pets_list = requests.get("http://localhost:8000/applicable_pets").json()
    return all_applicable_pets_list


@st.cache_resource
def get_products(search: str, app_pet: list[str]) -> list[dict[str, str]]:
    """
    Get products.

    Parameters
    ----------
    search: str
        The search string for the product title
    app_pet: list[str]
        Filter by applicable pet

    Returns
    -------
    List[dict]
        The products
    """
    params = {
        "search": search,
        "applicable_pet": ",".join(app_pet),
    }
    response = requests.get("http://localhost:8000/products", params=params)
    products = response.json()["products"]

    return products


@st.cache_resource
def get_product(mongo_id: str) -> dict[str, str]:
    """
    Get product.

    Parameters
    ----------
    mongo_id: str
        The MongoDB ID

    Returns
    -------
    Dict[str, str]
        The product
    """
    params = {"mongo_id": mongo_id}
    response = requests.get("http://localhost:8000/product", params=params)
    product_details = response.json()

    return product_details


def get_reviews(mongo_id: str, product_id: str, user_name: str) -> dict[str, str | dict[str, str]]:
    """
    Get reviews.

    Parameters
    ----------
    mongo_id: str
        The MongoDB ID
    product_id: str
        The product ID
    user_name: str
        The username

    Returns
    -------
    Dict[str, str | dict[str, str]]
        The reviews
    """
    params = {"mongo_id": mongo_id, "product_id": product_id, "user_name": user_name}
    response = requests.get("http://localhost:8000/reviews", params=params)
    reviews = response.json()

    return reviews


def post_review(product_id: str, nickname: str, review: str, rating: str) -> requests.Response:
    """
    Post reviews.

    Parameters
    ----------
    product_id: str
        The product ID
    nickname: str
        The nickname
    review: str
        The review
    rating: str
        The rating

    Returns
    -------
    requests.Response
        The response
    """
    payload = {
        "product_id": product_id,
        "nickname": nickname,
        "review": review,
        "rating": len(rating),
    }
    response = requests.post("http://localhost:8000/reviews", json=payload)
    return response


def delete_review():
    """Delete reviews."""
    pass
