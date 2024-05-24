import time
from math import ceil
from os import listdir

import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

from web.utils.auth import config_auth

st.set_page_config(
    page_title="Doge Market - Products", layout="wide", page_icon=":feet:", initial_sidebar_state="collapsed"
)
st.sidebar.header("Products")

st.markdown(
    """
        <style>
            button[title="View fullscreen"]{
                visibility: hidden;
            }
        </style>
        """,
    unsafe_allow_html=True,
)

with st.sidebar:
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    elif st.session_state["authentication_status"]:
        st.write(f"Welcome, {st.session_state['name']}!")
        st.write("Top picks for you:")
        authenticator = config_auth()
        authenticator.logout(location="sidebar")

if not st.session_state["authentication_status"]:
    st.error("You need to login to access this page")
    time.sleep(3)
    switch_page("Login")
else:
    st.subheader("The best products for your pet! :feet: :feet: :feet:", divider=True)
    with st.spinner("Loading the product list..."):
        ROW_SIZE = 5
        IMG_DIRECTORY = "img/products"
        files = listdir(IMG_DIRECTORY)
        time.sleep(2)

    expander = st.expander(label="Search and Filter", expanded=False)
    with expander:
        controls = st.columns(3, gap="small")
        with controls[0]:
            search = st.text_input("Search")
        with controls[1]:
            keywords = st.multiselect("Applicable Pet", ["dog", "cat", "rabbit", "hamster", "fish", "bird"])
        with controls[2]:
            batch_size = st.selectbox("Images per page:", range(25, 100, 25))
        num_batches = ceil(len(files) / batch_size)
        with controls[2]:
            page = st.selectbox("Page", range(1, num_batches + 1))

    grid = st.columns(ROW_SIZE)
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
                    switch_page("Product")

        col = (col + 1) % ROW_SIZE
