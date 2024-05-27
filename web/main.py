from time import sleep

import streamlit as st
from streamlit_server_state import no_rerun, server_state

from web.constants import FOOTER
from web.utils.pages import make_sidebar

st.set_page_config(
    layout="centered",
    page_icon=":feet:",
    page_title="Home",
    initial_sidebar_state="expanded",
)

make_sidebar()
st.markdown(
    "<h1>"
    '<img src="https://tung-local.myshopify.com/cdn/shop/products/Doge_1024x1024.png?v=1475122208" '
    'style="height:50px;">Doge Market</h1>',
    unsafe_allow_html=True,
)
if not server_state.get("authentication_status", False):
    with st.container(border=True):
        st.write("Please log in to continue (username `test`, password `test`).")
        st.info("You can also continue as a guest.")
        username = st.text_input("👤 :blue[**Username**]", help="Type your username")
        password = st.text_input("🔑 :red[**Password**]", type="password", help="Type your password")
        cols = st.columns(4)
        with cols[0]:
            login = st.button("Log in", type="primary", key="login", disabled=username == "" or password == "")
        with cols[1]:
            guest = st.button(
                "Continue as guest", type="secondary", key="guest", disabled=username != "" or password != ""
            )
        if login:
            if username == "test" and password == "test":
                with st.spinner("Checking credentials..."):
                    with no_rerun:
                        server_state.authentication_status = True
                        server_state.username = username
                        sleep(1.5)
                with st.spinner("Logged in successfully!"):
                    sleep(1.5)
                st.switch_page("pages/Products.py")
            else:
                with st.spinner("Checking credentials..."):
                    sleep(1.5)
                st.error("Incorrect username or password")

    if guest:
        with st.spinner("Redirecting to products page..."):
            with no_rerun:
                server_state.authentication_status = True
                server_state.username = "guest"
            sleep(1.5)
        st.switch_page("pages/Products.py")
else:
    with st.spinner("Redirecting to products page..."):
        sleep(1.5)
    st.switch_page("pages/Products.py")

st.markdown(FOOTER, unsafe_allow_html=True)
