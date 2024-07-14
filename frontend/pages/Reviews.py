import asyncio
import base64
import logging
from math import ceil

import streamlit as st
from streamlit_card import card

from frontend.constants import BATCH_SIZE_REVIEWS, FOOTER, ROW_SIZE_REVIEWS
from frontend.controller.products import get_product
from frontend.controller.reviews import delete_review
from frontend.controller.users import get_user_reviews
from frontend.utils.config import hide_image_fullscreen, make_sidebar

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def reviews_page() -> None:
    """Reviews page."""
    logger.info("Reviews page")
    st.set_page_config(
        layout="centered",
        page_icon="📝",
        page_title="Reviews",
        initial_sidebar_state="collapsed",
    )
    make_sidebar()
    hide_image_fullscreen()

    st.header("📝 Reviews")
    st.subheader("Your reviews", divider=True)

    page = st.session_state.get("page_reviews", 1)

    if st.session_state.get("username", None) is None:
        st.warning("Please log in to view your reviews.")
    else:
        grid = st.columns(ROW_SIZE_REVIEWS)
        reviews = get_user_reviews(st.session_state.get("username"))
        if page is None:
            st.info("No reviews yet. Go and find the products you love!")
            st.stop()
        num_batches = ceil(len(reviews) / BATCH_SIZE_REVIEWS)
        batch = reviews[(page - 1) * BATCH_SIZE_REVIEWS : page * BATCH_SIZE_REVIEWS]

        if len(reviews) > 0:
            col = 0
            for review in batch:
                _id_review = review["_id"]
                product_id = review["product_id"]
                product_details = await get_product({"product_id": product_id})
                title = product_details["title"]
                img_route = product_details["image_path"]
                _id_product = product_details["_id"]
                with grid[col]:
                    with st.container(border=True):
                        rev_cols = st.columns([2, 4, 1], gap="small")
                        s = ":star:" * review["rating"]
                        with rev_cols[0]:
                            with open(img_route, "rb") as f:
                                data = f.read()
                                encoded = base64.b64encode(data)
                            data = "data:image/png;base64," + encoded.decode("utf-8")
                            product_card = card(
                                title="",
                                text="",
                                image=data,
                                key=str(_id_review),
                                styles={
                                    "card": {
                                        "width": "100%",
                                        "height": "180px",
                                        "margin": "5%",
                                        "box-shadow": "0 0 15px rgba(0,0,0,0.5)",
                                        "display": "flex",
                                        "justify-content": "center",
                                    },
                                    "text": {"position": "absolute", "bottom": -100, "left": 0, "color": "black"},
                                    "filter": {"background-color": "rgba(0, 0, 0, 0)"},
                                },
                            )
                            if product_card:
                                st.session_state["_id"] = str(_id_product)
                                st.switch_page("pages/Product.py")
                        with rev_cols[1]:
                            st.html(f"<strong>{title}</strong>")
                            st.write(s)
                            st.html(f"<p><strong>\"{review['review']}\"</strong><em> on {review['date']}</em></p>")
                        with rev_cols[2]:
                            delete = st.button("❌", key=f"delete{str(_id_review)}", help="Delete review")

                        if delete:
                            await delete_review(_id_review, product_id, st.session_state.get("username"))
                            st.session_state.page_reviews = 1
                            st.rerun()

                col = (col + 1) % ROW_SIZE_REVIEWS
        else:
            st.info("No reviews yet. Go and find the products you love!")

        bottom = st.columns([10, 3, 10])
        with bottom[1]:
            page_select = st.selectbox(  # noqa
                "Page Number", range(1, num_batches + 1), key="page_reviews", disabled=num_batches == 1
            )
    st.markdown(FOOTER, unsafe_allow_html=True)


asyncio.run(reviews_page())
