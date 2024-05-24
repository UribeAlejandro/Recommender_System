import time

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from web.utils.auth import config_auth

prod = st.session_state["product_name"]
st.set_page_config(page_title=prod, layout="wide", page_icon=":feet:", initial_sidebar_state="collapsed")
st.sidebar.header("Product")

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
    st.subheader(f"Product name: {prod}", divider=True)
    back_to_products = st.button("Back to products")
    if back_to_products:
        switch_page("Products")
    with st.spinner("Loading the product details..."):
        time.sleep(2)
        st.write("Product details here")
        st.write("Product images here")
        st.write("Product price here")
        st.write("Product rating here")
        st.write("Product reviews here")
        st.write("Product description here")
        st.write("Product specifications here")
        st.write("Product availability here")
        st.write("Product shipping details here")
        st.write("Product seller details here")
        st.write("Product similar products here")
        st.write("Product related products here")
        st.write("Product recommended products here")
        st.write("Product categories here")
        st.write("Product tags here")
        st.write("Product colors here")
        st.write("Product sizes here")
        st.write("Product materials here")
        st.write("Product brand here")
        st.write("Product manufacturer here")
        st.write("Product country here")
        st.write("Product weight here")
        st.write("Product dimensions here")
        st.write("Product care instructions here")
        st.write("Product warranty here")
        st.write("Product return policy here")
        st.write("Product refund policy here")
        st.write("Product exchange policy here")
        st.write("Product cancellation policy here")
        st.write("Product payment methods here")
        st.write("Product delivery methods here")
        st.write("Product order tracking here")
        st.write("Product customer service here")
        st.write("Product customer reviews here")
        st.write("Product customer ratings here")
        st.write("Product customer testimonials here")
        st.write("Product customer photos here")
        st.write("Product customer videos here")
        st.write("Product customer feedback here")
        st.write("Product customer complaints here")
        st.write("Product customer queries here")
        st.write("Product customer support here")
        st.write("Product customer care here")
        st.write("Product customer satisfaction here")
        st.write("Product customer loyalty here")
        st.write("Product customer retention here")
        st.write("Product customer acquisition here")
        st.write("Product customer engagement here")
        st.write("Product customer experience here")
        st.write("Product customer journey here")
        st.write("Product customer relationship here")
        st.write("Product customer interaction here")
        st.write("Product customer communication here")
        st.write("Product customer collaboration here")
        st.write("Product customer empowerment here")
