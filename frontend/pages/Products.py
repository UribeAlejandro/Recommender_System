import base64
from math import ceil

import streamlit as st
from streamlit_card import card
from streamlit_server_state import no_rerun

from frontend.constants import FOOTER, ROW_SIZE
from frontend.pages.config import hide_image_fullscreen, make_sidebar
from frontend.utils.backend import get_all_applicable_pets, get_products

st.set_page_config(
    layout="wide",
    page_icon="🎁",
    page_title="Products",
    initial_sidebar_state="collapsed",
)

make_sidebar()
hide_image_fullscreen()

search = st.session_state.get("search", "")
app_pet = st.session_state.get("app_pet", [])
page = st.session_state.get("page", 1)
sort = st.session_state.get("sort", "Relevance")

st.header("🎁 Product List")
st.subheader("Your one-stop shop for all things!", divider=True)
with st.spinner("Loading the product list..."):
    all_applicable_pets = get_all_applicable_pets()
    sort_options = [
        "Relevance",
        "Price: Low to High",
        "Price: High to Low",
        "Discount: High to Low",
        "Discount: Low to High",
        "Alphabetical: A-Z",
        "Alphabetical: Z-A",
    ]
    sort_index = sort_options.index(sort)
    products = get_products(search, app_pet)

    expander = st.expander(label="Search and Filter", expanded=True)

    with expander:
        controls = st.columns([3, 2, 2, 2, 2], gap="small")

        with controls[0]:
            st.markdown("**Product name**")
            search = st.text_input(
                "Product name", key="search", placeholder="Search for a product...", label_visibility="collapsed"
            )
        with controls[1]:
            st.markdown("**Sort by**")
            sort = st.selectbox("Sort by:", sort_options, index=sort_index, key="sort", label_visibility="collapsed")
            if sort == "Alphabetical: A-Z":
                products = sorted(products, key=lambda x: x["title"])
            elif sort == "Alphabetical: Z-A":
                products = sorted(products, key=lambda x: x["title"], reverse=True)
            elif sort == "Price: Low to High":
                products = sorted(products, key=lambda x: x["price_discount"], reverse=False)
            elif sort == "Price: High to Low":
                products = sorted(products, key=lambda x: x["price_discount"], reverse=True)
            elif sort == "Discount: High to Low":
                products = sorted(products, key=lambda x: x["off_percent"] if x["off_percent"] else 0, reverse=False)
            elif sort == "Discount: Low to High":
                products = sorted(products, key=lambda x: x["off_percent"] if x["off_percent"] else 0, reverse=True)
            elif sort == "Relevance":
                products = sorted(products, key=lambda x: x["id"])
        with controls[2]:
            st.markdown("**Category**")
            category = st.multiselect(
                "Category", options=all_applicable_pets, key="category", label_visibility="collapsed"
            )
        with controls[3]:
            st.markdown("**Applicable Pet**")
            app_pet = st.multiselect(
                "Applicable Pet", options=all_applicable_pets, key="app_pet", label_visibility="collapsed"
            )
        with controls[4]:
            st.markdown("**Images per page**")
            batch_size = st.selectbox(
                "Images per page",
                range(20, 100, 20),
                key="batch_size",
                label_visibility="collapsed",
                disabled=len(products) < st.session_state.get("batch_size", 20),
            )

    if len(products) == 0:
        st.error("No products found.")
        st.stop()

    st.success(f"We have {len(products)} for your pet! 🐶🐱🐹🐰🐦🐢🐍🐠🦎🐾🦜🐴🐷🐄🐑🐓🦃🦢🦆🦉🦚🦜🦇🦋🐝🐞🦗🕷🦟🦠")
    grid = st.columns(ROW_SIZE)
    num_batches = ceil(len(products) / batch_size)
    batch = products[(page - 1) * batch_size : page * batch_size]

    col = 0
    for product in batch:
        with grid[col]:
            _id = product["id"]
            title = product["title"]
            img_route = product["image_path"]
            price_discount = product["price_discount"]
            price_real = product.get("price_real")
            off_percent = product.get("off_percent", 0)
            __off_percent = f"{off_percent}% off" if off_percent else ""

            with open(img_route, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data)
            data = "data:image/png;base64," + encoded.decode("utf-8")

            with st.container(height=370):
                product_card = card(
                    title=f"{__off_percent}",
                    text=f"${price_discount}",
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
                        "text": {"position": "absolute", "bottom": 0, "left": 50, "color": "green"},
                        "title": {"position": "absolute", "bottom": 120, "right": 15, "color": "red"},
                        "filter": {"background-color": "rgba(0, 0, 0, 0)"},
                    },
                )
                st.write(title[0:90])

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
