import base64
import random
from math import ceil

import streamlit as st
from pymongo.errors import ServerSelectionTimeoutError
from streamlit_card import card
from streamlit_server_state import no_rerun

from web.constants import COLLECTION_DETAILS, DATABASE_NAME, FOOTER, ROW_SIZE
from web.utils.database import get_mongo_database
from web.utils.pages import hide_image_fullscreen, make_sidebar

st.set_page_config(
    layout="wide",
    page_icon="🎁",
    page_title="Products",
    initial_sidebar_state="collapsed",
)

make_sidebar()
hide_image_fullscreen()

st.header("🎁 Product List")
st.subheader("Your one-stop shop for all things!", divider=True)
with st.spinner("Loading the product list..."):
    try:
        db = get_mongo_database(DATABASE_NAME)
        collection = db.get_collection(COLLECTION_DETAILS)
        all_applicable_pets = collection.distinct("description_items.applicable pet")
        filter_dict = {
            "$and": [
                {"image_path": {"$exists": True}},
                {"image_path": {"$ne": "pending"}},
                {"title": {"$regex": st.session_state.get("search", ""), "$options": "i"}},
                {"description_items.applicable pet": {"$in": st.session_state.get("app_pet", all_applicable_pets)}},
            ]
        }
        products = collection.find(
            filter_dict,
            {"description_items.applicable pet": 1, "image_path": 1, "title": 1, "product_id": 1, "_id": 1},
        )
        products = list(products)
        applicable_pets = set(list(prod["description_items"]["applicable pet"] for prod in products))

    except ServerSelectionTimeoutError:
        st.error("Error connecting to the database. Please try again later.")
        st.stop()

    expander = st.expander(label="Search and Filter", expanded=False)

    with expander:
        controls = st.columns([4, 2, 2, 1], gap="small")
        with controls[0]:
            search = st.text_input("Product name", key="search", placeholder="Search for a product...")
        with controls[1]:
            sort = st.selectbox(
                "Sort by:", ["Relevance", "A-Z", "Z-A", "Price: Low to High", "Price: High to Low"], key="sort"
            )
            if sort == "A-Z":
                products = sorted(products, key=lambda x: x["title"])
            elif sort == "Z-A":
                products = sorted(products, key=lambda x: x["title"], reverse=True)
            elif sort == "Relevance":
                products = sorted(products, key=lambda x: x["_id"])
            elif sort == "Price: Low to High":
                products = sorted(products, key=lambda x: x["_id"], reverse=True)
            elif sort == "Price: High to Low":
                products = sorted(products, key=lambda x: x["_id"], reverse=False)

        with controls[2]:
            app_pet = st.multiselect(
                "Applicable Pet", options=all_applicable_pets, default=applicable_pets, key="app_pet"
            )
        with controls[3]:
            batch_size = st.selectbox(
                "Images per page:",
                range(20, 100, 20),
                disabled=len(products) < st.session_state.get("batch_size", 20),
                key="batch_size",
            )

    if len(products) == 0:
        st.error("No products found.")
        st.stop()

    grid = st.columns(ROW_SIZE)
    page = st.session_state.get("page", 1)
    num_batches = ceil(len(products) / batch_size)
    batch = products[(page - 1) * batch_size : page * batch_size]

    col = 0
    for product in batch:
        with grid[col]:
            _id = product["_id"]
            title = product["title"]
            img_route = product["image_path"]

            with open(img_route, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data)
            data = "data:image/png;base64," + encoded.decode("utf-8")

            with st.container(height=450):
                product_card = card(
                    title="",
                    text="",
                    image=data,
                    key=str(_id),
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "180px",
                            "margin": "0%",
                            "box-shadow": "0 0 5px rgba(0,0,0,0.5)",
                            "display": "inline-flex",
                            "justify-content": "center",
                        },
                        "text": {"position": "absolute", "bottom": 0, "left": 15, "color": "red"},
                        "filter": {"background-color": "rgba(0, 0, 0, 0)"},
                    },
                )

                cols = st.columns([2, 4, 1])
                with cols[1]:
                    off = int(random.uniform(0.5, 1) * 100)
                    st.metric(
                        label="price",
                        value="",
                        delta=f"{str(-off)}% OFF",
                        delta_color="normal",
                        label_visibility="hidden",
                    )
                    st.markdown("*💸:green[2.5USD]💸*")
                st.write(title)
                if product_card:
                    with no_rerun:
                        st.session_state["_id"] = _id
                    st.switch_page("pages/Product.py")

        col = (col + 1) % ROW_SIZE
    st.divider()
    bottom = st.columns(7)
    with bottom[6]:
        page_select = st.selectbox("Page Number", range(1, num_batches + 1), key="page", disabled=num_batches == 1)

st.markdown(FOOTER, unsafe_allow_html=True)
