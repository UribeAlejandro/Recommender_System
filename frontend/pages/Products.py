import base64
from math import ceil

import streamlit as st
from streamlit_card import card
from streamlit_server_state import no_rerun

from frontend.constants import FOOTER, ROW_SIZE
from frontend.utils.config import hide_image_fullscreen, make_sidebar
from frontend.utils.controller import get_products

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
page_size = st.session_state.get("batch_size", 20)
sort_key = st.session_state.get("sort", "Relevance")
category = st.session_state.get("category", [])
subcategory = st.session_state.get("subcategory", [])

st.header("🎁 Product List")
st.subheader("Your one-stop shop for all things!", divider=True)
with st.spinner("Loading the product list..."):
    sort_options = [
        "Relevance",
        "Highest Discount",
        "Alphabetical: A-Z",
        "Alphabetical: Z-A",
        "Price: Low to High",
        "Price: High to Low",
    ]

    response = get_products(search, sort_key, app_pet, category, subcategory, page_size, page)

    products = response["items"]
    number = response["number"]
    all_applicable_pets = response["applicable_pets"]
    categories = response["categories"]
    subcategories = response["subcategories"]
    more_pages = response["more_pages"]

    expander = st.expander(label="**Search and Filter**", expanded=True)

    with expander:
        controls = st.columns([3, 2, 2], gap="small")

        with controls[0]:
            st.markdown("**Product name**")
            search = st.text_input(
                "Product name", key="search", placeholder="Search for a product...", label_visibility="collapsed"
            )
        with controls[0]:
            st.markdown("**Sort by**")
            sort = st.selectbox("Sort by:", sort_options, key="sort", label_visibility="collapsed")
        with controls[1]:
            st.markdown("**Category**")
            category = st.multiselect("Category", options=categories, key="category", label_visibility="collapsed")
            st.markdown("**Subcategory**")
            subcategory = st.multiselect(
                "SubCategory", options=subcategories, key="subcategory", label_visibility="collapsed"
            )
        with controls[2]:
            st.markdown("**Applicable Pet**")
            app_pet = st.multiselect(
                "Applicable Pet", options=all_applicable_pets, key="app_pet", label_visibility="collapsed"
            )
        with controls[2]:
            st.markdown("**Images per page**")
            page_size = st.selectbox(
                "Images per page",
                range(20, 100, 20),
                key="batch_size",
                label_visibility="collapsed",
                disabled=not more_pages,
            )

    if number == 0:
        st.error("No products found.")
        st.stop()

    st.success(f"We have {number} for your pet! 🐶🐱🐹🐰🐦🐢🐍🐠🦎🐾🦜🐴🐷🐄🐑🐓🦃🦢🦆🦉🦚🦜🦇🦋🐝🐞🦗🕷🦟🦠")
    grid = st.columns(ROW_SIZE)
    num_batches = ceil(number / page_size)

    col = 0
    for product in products:
        with grid[col]:
            _id = product["_id"]
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
