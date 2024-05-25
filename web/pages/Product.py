import time

import streamlit as st
from PIL import Image
from streamlit_server_state import server_state

from web.constants import COLLECTION_DETAILS, DATABASE_NAME
from web.utils.database import get_mongo_database
from web.utils.pages import css, make_sidebar

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
        initial_sidebar_state="expanded",
    )
    make_sidebar()
    css()

db = get_mongo_database(DATABASE_NAME)
collection = db.get_collection(COLLECTION_DETAILS)
product = collection.find_one({"product_id": product_id})
title = product["title"]
img_route = product["image_path"]
product_id = product["product_id"]

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
        with st.expander(":blue[**Description**]", expanded=True):
            col1, col2 = st.columns(2)
            for k, v in product_description.items():
                with col1:
                    st.write(f"**{str(k).capitalize()}**")
                with col2:
                    st.write(f"*{str(v).capitalize()}*")
