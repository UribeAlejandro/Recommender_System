import time
from datetime import datetime
from math import ceil

import streamlit as st
from PIL import Image
from streamlit_server_state import server_state

from frontend.constants import COLLECTION_DETAILS, COLLECTION_REVIEWS, DATABASE_NAME, FOOTER
from frontend.utils.database import get_mongo_database
from frontend.utils.pages import hide_image_fullscreen, make_sidebar

_id = st.session_state.get("_id", None)

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
    db = get_mongo_database(DATABASE_NAME)
    collection_reviews = db.get_collection(COLLECTION_REVIEWS)
    collection_products = db.get_collection(COLLECTION_DETAILS)

    product_details = collection_products.find_one({"_id": _id})

    title = product_details["title"]
    img_route = product_details["image_path"]
    product_id = product_details["product_id"]
    price_discount = product_details.get("price_discount")
    price_real = product_details.get("price_real", price_discount)
    off_percent = product_details.get("off_percent", "0%")

    already_reviewed = collection_reviews.find_one({"product_id": product_id, "nickname": server_state.get("username")})
    mean_rating = collection_reviews.aggregate(
        [{"$match": {"product_id": product_id}}, {"$group": {"_id": _id, "mean": {"$avg": "$rating"}}}]
    )
    mean_rating = next(mean_rating, {"mean": 0})

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
                    st.markdown(f"**:green[${price_discount}]** ~~${price_real}~~")
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
                        s = ":star:" * already_reviewed["rating"]
                        with rev_cols[0]:
                            st.write(f"**{already_reviewed['nickname']}** *{already_reviewed['date']}*")
                            st.write(s)
                        with rev_cols[1]:
                            st.write(f"*{already_reviewed['review']}*")

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
                                collection_reviews.insert_one(
                                    {
                                        "product_id": product_id,
                                        "nickname": server_state.get("username"),
                                        "review": review,
                                        "rating": len(rating),
                                        "date": time.strftime("%d %b, %Y"),
                                        "timestamp": datetime.now(),
                                    }
                                )
                                st.rerun()
    st.divider()
    st.subheader("Product reviews", divider=False)
    st.markdown(f"<h4>Mean rating: {mean_rating['mean']:.2f} ⭐</h4>", unsafe_allow_html=True)

    reviews = list(collection_reviews.find({"product_id": product_details["product_id"]}).sort({"timestamp": -1}))
    ROW_SIZE = 1
    batch_size = 5
    grid = st.columns(ROW_SIZE)
    page = st.session_state.get("page_reviews", 1)
    num_batches = ceil(len(reviews) / batch_size)
    batch = reviews[(page - 1) * batch_size : page * batch_size]

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
            col = (col + 1) % ROW_SIZE
    else:
        st.write("No reviews yet. Be the first to review this product!")

    bottom = st.columns([10, 3, 10])
    with bottom[1]:
        page_select = st.selectbox(
            "Page Number", range(1, num_batches + 1), key="page_reviews", disabled=num_batches == 1
        )

st.divider()
st.markdown(FOOTER, unsafe_allow_html=True)
