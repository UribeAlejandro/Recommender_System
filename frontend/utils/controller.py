from datetime import datetime

import requests

from frontend.constants import BACKEND_URL


def get_products(
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
    response = requests.get(f"{BACKEND_URL}/products/", params=params)
    response = response.json()

    return response


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


def get_reviews(product_id: str, user_name: str) -> dict[str, str | dict[str, str]]:
    """
    Get reviews.

    Parameters
    ----------
    product_id: str
        The product ID
    user_name: str
        The username

    Returns
    -------
    Dict[str, str | dict[str, str]]
        The reviews
    """
    params = {"product_id": product_id, "user_name": user_name}
    response = requests.get(f"{BACKEND_URL}/reviews/", params=params)
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
        "timestamp": datetime.now().isoformat(),
    }
    response = requests.post(f"{BACKEND_URL}/reviews/", json=payload)
    return response


def delete_review(mongo_id: str, product_id: str, nickname: str) -> requests.Response:
    """Delete reviews.

    Parameters
    ----------
    mongo_id: str
        The MongoDB ID
    product_id: str
        The product ID
    nickname: str
        The nickname

    Returns
    -------
    requests.Response
        The response
    """
    params = {"mongo_id": str(mongo_id), "product_id": product_id, "nickname": nickname}
    r = requests.delete(f"{BACKEND_URL}/reviews/", params=params)
    return r


def get_user_reviews(nickname: str) -> list[dict]:
    """
    Get user reviews.

    Parameters
    ----------
    nickname: str
        The nickname

    Returns
    -------
    List[dict]
        The reviews
    """
    params = {"nickname": nickname}
    response = requests.get(f"{BACKEND_URL}/user/reviews/", params=params)
    reviews = response.json()
    return reviews


def get_recommendations(nickname: str) -> list[dict]:
    """
    Get recommendations.

    Parameters
    ----------
    nickname: str
        The nickname

    Returns
    -------
    List[dict]
        The recommendations
    """
    params = {"nickname": nickname}
    products_req = requests.get(f"{BACKEND_URL}/recommender/", params=params)
    products_json = products_req.json()

    return products_json


def get_rating_charts() -> dict:
    """
    Get rating charts.

    Returns
    -------
    Dict
        The rating charts
    """
    response = requests.get(f"{BACKEND_URL}/stats/")
    rating_charts = response.json()

    return rating_charts


def get_similar_products(mongo_id: str) -> list[dict]:
    """
    Get similar products.

    Parameters
    ----------
    mongo_id: str
        The product MongoDB ID

    Returns
    -------
    List[dict]
        The similar products
    """
    params = {"mongo_id": mongo_id}
    response = requests.get(f"{BACKEND_URL}/recommender/similar", params=params)
    similar_products = response.json()

    return similar_products
