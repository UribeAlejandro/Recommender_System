import time

import streamlit as st

from web.utils.pages import css, make_sidebar

st.session_state["authentication_status"] = st.session_state.get("authentication_status", False)
st.session_state["username"] = st.session_state.get("username", "guest")

prod = st.session_state.get("product_name", False)


if not prod:
    st.error("Product not found. Please select a product from the list.")
    with st.spinner("Redirecting to products page..."):
        time.sleep(2)
    st.switch_page("pages/2_Products.py")
else:
    st.set_page_config(page_title=prod, layout="wide", page_icon=":feet:", initial_sidebar_state="collapsed")

    make_sidebar()
css()

st.subheader(f"Product name: {prod}", divider=True)

with st.spinner("Loading the product details..."):
    time.sleep(1.5)
    st.write("Product details here")
    st.write("Product images here")
    st.write("Product price here")
    st.write("Product rating here")
