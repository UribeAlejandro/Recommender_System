import base64
from math import ceil

import streamlit as st
from streamlit_card import card
from streamlit_server_state import no_rerun, server_state

from web.constants import COLLECTION_DETAILS, DATABASE_NAME, FOOTER, ROW_SIZE
from web.utils.database import get_mongo_database
from web.utils.pages import hide_image_fullscreen, make_sidebar

st.set_page_config(
    layout="wide",
    page_icon="🎁",
    page_title="Products",
    initial_sidebar_state="auto",
)

make_sidebar()
hide_image_fullscreen()

st.header("🎁 Product List")
st.subheader("Your one-stop shop for all things!", divider=True)
with st.spinner("Loading the product list..."):
    db = get_mongo_database(DATABASE_NAME)
    collection = db.get_collection(COLLECTION_DETAILS)
    products = collection.find(
        {"$and": [{"image_path": {"$exists": True}}, {"image_path": {"$ne": "pending"}}]},
        {"image_path": 1, "product_id": 1, "title": 1, "_id": False},
    )
    products = list(products)

    expander = st.expander(label="Search and Filter", expanded=False)

    with expander:
        controls = st.columns(3, gap="small")
        with controls[0]:
            search = st.text_input("Search")
        with controls[1]:
            keywords = st.multiselect("Applicable Pet", ["dog", "cat", "rabbit", "hamster", "fish", "bird"])
        with controls[2]:
            batch_size = st.selectbox("Images per page:", range(20, 100, 20))

    grid = st.columns(ROW_SIZE)
    page = st.session_state.get("page", 1)
    num_batches = ceil(len(products) / batch_size)
    batch = products[(page - 1) * batch_size : page * batch_size]

    col = 0
    for product in batch:
        with grid[col]:
            title = product["title"]
            img_route = product["image_path"]
            product_id = product["product_id"]

            with open(img_route, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data)
            data = "data:image/png;base64," + encoded.decode("utf-8")

            with st.container(height=400):
                hasClicked = card(
                    title="",
                    text="",
                    image=data,
                    key=product_id,
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "200px",
                            "margin": "5%",
                            "box-shadow": "0 0 15px rgba(0,0,0,0.5)",
                            "display": "flex",
                            "justify-content": "center",
                        },
                        "text": {"position": "absolute", "bottom": -100, "left": 0, "color": "black"},
                        "filter": {"background-color": "rgba(0, 0, 0, 0)"},
                    },
                )
                st.write(title)
                if hasClicked:
                    with no_rerun:
                        server_state["product_id"] = product_id
                        server_state["title"] = title
                    st.switch_page("pages/Product.py")
            #     st.image(new_image)
            #     caption = st.button(title, key=product_id)
            #     if caption:
            #         st.query_params["product_id"] = product_id
            #         st.query_params["title"] = title
            #         st.switch_page("pages/Product.py")

        col = (col + 1) % ROW_SIZE

    st.divider()
    bottom = st.columns(7)
    with bottom[6]:
        page_select = st.selectbox("Page Number", range(1, num_batches + 1), key="page", disabled=num_batches == 1)

st.markdown(FOOTER, unsafe_allow_html=True)
