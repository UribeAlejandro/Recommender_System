import requests
import streamlit as st

from frontend.constants import BACKEND_URL


@st.cache_resource
def get_all_applicable_pets() -> list[str]:
    """
    Get all applicable pets.

    Returns
    -------
    list
        The list of applicable pets
    """
    all_applicable_pets_list = requests.get(f"{BACKEND_URL}/applicable_pets").json()
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
    response = requests.get(f"{BACKEND_URL}/products", params=params)
    products = response.json()["products"]

    return products


@st.cache_resource
def get_product(filter_dict: dict) -> dict[str, str]:
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
    response = requests.post(f"{BACKEND_URL}/products/details", json=filter_dict)
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
    response = requests.get(f"{BACKEND_URL}/reviews", params=params)
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
    response = requests.post(f"{BACKEND_URL}/reviews", json=payload)
    return response


def delete_review(mongo_id: str, product_id: str, nickname: str) -> requests.Response:
    """Delete reviews."""
    params = {"mongo_id": str(mongo_id), "product_id": product_id, "nickname": nickname}
    r = requests.delete(f"{BACKEND_URL}/reviews", params=params)
    return r


def get_user_reviews(nickname: str):
    """Get user reviews."""
    params = {"nickname": nickname}
    response = requests.get(f"{BACKEND_URL}/user/reviews", params=params)
    reviews = response.json()
    return reviews
