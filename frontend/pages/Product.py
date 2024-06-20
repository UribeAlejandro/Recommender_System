import time
from math import ceil

import streamlit as st
from PIL import Image
from streamlit_server_state import server_state

from frontend.constants import BATCH_SIZE_PRODUCT_REVIEWS, FOOTER, ROW_SIZE_PRODUCT_REVIEWS
from frontend.utils.config import hide_image_fullscreen, make_sidebar
from frontend.utils.controller import get_product, get_reviews, post_review

_id = st.session_state.get("_id", None)
page = st.session_state.get("page_reviews", 1)

if not _id:
    st.error("Product not found. Please select a product from the list.")
    with st.spinner("Redirecting to products page..."):
        time.sleep(1.5)
    st.switch_page("pages/Products.py")
else:
    st.set_page_config(
        page_title=st.session_state.get("title", "Product Details"),
        layout="wide",
        page_icon=":feet:",
        initial_sidebar_state="collapsed",
    )
    make_sidebar()
    hide_image_fullscreen()

back = st.button("Back to products", key="back", type="primary")
if back:
    st.switch_page("pages/Products.py")

with st.spinner("Loading the product details..."):
    product_details = get_product({"_id": str(_id)})

    title = product_details["title"]
    img_route = product_details["image_path"]
    product_id = product_details["product_id"]

    price_discount = product_details.get("price_discount")
    price_real = product_details.get("price_real")
    off_percent = product_details.get("off_percent", 0)

    price_discount = f"${price_discount:.2f}" if price_discount else "N/A"
    price_real = f"~~${price_real:.2f}~~" if price_real else ""
    off_percent = f"{off_percent}%" if off_percent else "N/A"

    user_name = server_state.get("username")
    reviews = get_reviews(product_id, user_name)

    already_reviewed = reviews.get("already_reviewed", {})
    mean_rating = reviews.get("mean_rating", 0.0)

    st.subheader(title, divider=True)
    cols = st.columns([2, 1, 3], gap="small")

    with cols[0]:
        image = Image.open(img_route)
        st.image(image, use_column_width="always")
        st.caption("Other products are not included in the purchase.")

    with cols[2]:
        st.subheader("Product description", divider=False)
        product_description = product_details["description_items"]
        with st.container():
            with st.expander(":blue[**Description**]", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Discount**")
                    st.write("**Price**")
                    st.write("**Product ID**")
                with col2:
                    st.markdown(f"**:red[{off_percent}]**")
                    st.markdown(f"**:green[{price_discount}]** {price_real}")
                    st.write(f"*{product_id}*")
                for k, v in product_description.items():
                    with col1:
                        st.write(f"**{str(k).capitalize()}**")
                    with col2:
                        st.write(f"{str(v).capitalize()}")
            st.divider()
            st.markdown("<h4>Review this product!</h4>", unsafe_allow_html=True)
            if server_state.get("username") == "guest":
                st.error("You need to be logged in to review this product.")
            else:
                if already_reviewed:
                    st.write("You have already reviewed this product.")
                    with st.container(border=True):
                        rev_cols = st.columns(2, gap="small")
                        s = ":star:" * already_reviewed[0]["rating"]
                        with rev_cols[0]:
                            st.write(f"**{already_reviewed[0]['nickname']}** *{already_reviewed[0]['date']}*")
                            st.write(s)
                        with rev_cols[1]:
                            st.write(f"*{already_reviewed[0]['review']}*")

                    go_to_reviews = st.button("Go to your reviews", key="go_to_reviews", type="secondary")
                    if go_to_reviews:
                        st.switch_page("pages/Reviews.py")

                else:
                    with st.form(key="review_form", clear_on_submit=True):
                        review_cols = st.columns([10, 1], gap="small")
                        with review_cols[0]:
                            rating_options = [i * "⭐" for i in range(1, 6)]
                            rating = st.select_slider(
                                "Rating",
                                key="rating",
                                value=rating_options[2],
                                options=rating_options,
                                label_visibility="hidden",
                            )
                            review = st.text_area(
                                "Review", key="review", max_chars=500, placeholder="Your review here..."
                            )
                            submit = st.form_submit_button("Submit")
                            if submit:
                                nickname = server_state.get("username")
                                response = post_review(product_id, nickname, review, rating)
                                if response.status_code == 201:
                                    st.success("Review submitted successfully!")
                                else:
                                    st.error("Failed to submit review. Please try again.")
                                st.rerun()
    st.divider()
    st.subheader("Product reviews", divider=False)
    st.markdown(f"<h4>Mean rating: {mean_rating:.1f} ⭐</h4>", unsafe_allow_html=True)

    reviews = reviews.get("reviews", [])
    grid = st.columns(ROW_SIZE_PRODUCT_REVIEWS)
    num_batches = ceil(len(reviews) / BATCH_SIZE_PRODUCT_REVIEWS)
    batch = reviews[(page - 1) * BATCH_SIZE_PRODUCT_REVIEWS : page * BATCH_SIZE_PRODUCT_REVIEWS]

    if len(reviews) > 0:
        col = 0
        for review in batch:
            with grid[col]:
                with st.container(border=True):
                    rev_cols = st.columns(2, gap="small")
                    s = ":star:" * review["rating"]
                    with rev_cols[0]:
                        st.write(f"**{review['nickname']}** *{review['date']}*")
                        st.write(s)
                    with rev_cols[1]:
                        st.write(f"*{review['review']}*")
            col = (col + 1) % ROW_SIZE_PRODUCT_REVIEWS
    else:
        st.info("No reviews yet. Be the first to review this product!")

    bottom = st.columns([10, 3, 10])
    with bottom[1]:
        page_select = st.selectbox(
            "Page Number", range(1, num_batches + 1), key="page_reviews", disabled=num_batches == 1
        )

st.divider()
st.markdown(FOOTER, unsafe_allow_html=True)
