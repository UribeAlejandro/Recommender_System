import time
from math import ceil

import streamlit as st
from PIL import Image
from streamlit_server_state import server_state

from web.constants import COLLECTION_DETAILS, COLLECTION_REVIEWS, DATABASE_NAME, FOOTER
from web.utils.database import get_mongo_database
from web.utils.pages import hide_image_fullscreen, make_sidebar

product_id = server_state.get("product_id", None)

if not product_id:
    st.error("Product not found. Please select a product from the list.")
    with st.spinner("Redirecting to products page..."):
        time.sleep(1.5)
    st.switch_page("pages/Products.py")
else:
    st.set_page_config(
        page_title=server_state.get("title", "Product"),
        layout="wide",
        page_icon=":feet:",
        initial_sidebar_state="auto",
    )
    make_sidebar()
    hide_image_fullscreen()

db = get_mongo_database(DATABASE_NAME)
products_collection = db.get_collection(COLLECTION_DETAILS)
product_reviews = db.get_collection(COLLECTION_REVIEWS)
product = products_collection.find_one({"product_id": product_id})
reviews = list(product_reviews.find({"product_id": product_id}))
title = product["title"]
img_route = product["image_path"]
product_id = product["product_id"]


back = st.button("Back to products", key="back", type="secondary")
if back:
    st.switch_page("pages/Products.py")
st.header(title, divider=True)
with st.spinner("Loading the product details..."):
    cols = st.columns(3, gap="small")
    time.sleep(1.5)

    with cols[0]:
        image = Image.open(img_route)
        st.image(image, use_column_width="never")
    with cols[1]:
        st.subheader("Product description", divider=False)
        product_description = product["description_items"]
        with st.container():
            with st.expander(":blue[**Description**]", expanded=True):
                col1, col2 = st.columns(2)
                for k, v in product_description.items():
                    with col1:
                        st.write(f"**{str(k).capitalize()}**")
                    with col2:
                        st.write(f"*{str(v).capitalize()}*")
    with cols[2]:
        st.markdown("<h4>How much do you like this product?</h4>", unsafe_allow_html=True)
        star_cols = st.columns(5, gap="small")
        stars = [
            st.button(":star:" * i, key=f"rating_{i}", type="secondary", disabled=st.session_state.get("rating", False))
            for i in range(1, 6)
        ]
        with star_cols[0]:
            one_star = stars[0]
        with star_cols[1]:
            two_star = stars[1]
        with star_cols[2]:
            three_star = stars[2]
        with star_cols[3]:
            four_star = stars[3]
        with star_cols[4]:
            five_star = stars[4]

    if one_star:
        st.session_state["rating"] = 1
        print("One star")
        st.rerun()
    if two_star:
        st.session_state["rating"] = 2
        print("Two star")
        st.rerun()
    if three_star:
        st.session_state["rating"] = 3
        print("Three star")
        st.rerun()
    if four_star:
        st.session_state["rating"] = 4
        print("Four star")
        st.rerun()
    if five_star:
        st.session_state["rating"] = 5
        print("Five star")
        st.rerun()

    st.divider()
    st.subheader("Product reviews", divider=False)

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

    st.divider()
    bottom = st.columns(7)
    with bottom[6]:
        page_select = st.selectbox(
            "Page Number", range(1, num_batches + 1), key="page_reviews", disabled=num_batches == 1
        )
st.markdown(FOOTER, unsafe_allow_html=True)
