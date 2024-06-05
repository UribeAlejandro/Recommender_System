from fastapi import APIRouter

router = APIRouter()


@router.get("/products")
async def products() -> dict:
    """
    Get products.

    Returns
    -------
    dict
        The products
    """
    return {"products": []}
