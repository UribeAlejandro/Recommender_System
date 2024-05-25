import time
from math import ceil

import streamlit as st
from PIL import Image

from web.constants import IMG_DIRECTORY
from web.utils.database import get_files
from web.utils.pages import css, make_sidebar

st.set_page_config(
    layout="wide",
    page_icon=":feet:",
    page_title="Products",
    initial_sidebar_state="collapsed",
)

css()
make_sidebar()


st.subheader("The best products for your pet! :feet: :feet: :feet:", divider=True)
with st.spinner("Loading the product list..."):
    ROW_SIZE = 5
    files = get_files()
    time.sleep(1.5)

    expander = st.expander(label="Search and Filter", expanded=False)

    with expander:
        controls = st.columns(3, gap="small")
        with controls[0]:
            search = st.text_input("Search")
        with controls[1]:
            keywords = st.multiselect("Applicable Pet", ["dog", "cat", "rabbit", "hamster", "fish", "bird"])
        with controls[2]:
            batch_size = st.selectbox("Images per page:", range(25, 150, 25))

    grid = st.columns(ROW_SIZE)
    page = st.session_state.get("page", 1)
    num_batches = ceil(len(files) / batch_size)
    batch = files[(page - 1) * batch_size : page * batch_size]

    col = 0
    for image in batch:
        with grid[col]:
            route = f"{IMG_DIRECTORY}/{image}"
            image = Image.open(route)
            new_image = image.resize((200, 200))
            with st.container(height=300):
                st.image(new_image)
                caption = st.button("Bike", key=route)
                if caption:
                    st.session_state["product_name"] = "Bike1"
                    st.switch_page("pages/Product.py")

        col = (col + 1) % ROW_SIZE

    st.divider()
    bottom = st.columns(6)
    with bottom[2]:
        page_select = st.selectbox("Page Number", range(1, num_batches + 1), key="page", disabled=num_batches == 1)
