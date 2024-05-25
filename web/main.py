from time import sleep

import streamlit as st

from web.utils.pages import make_sidebar

st.set_page_config(
    layout="wide",
    page_icon=":feet:",
    page_title="Products",
    initial_sidebar_state="expanded",
)

make_sidebar()

st.title("Welcome to Doge Market")
st.write("Please log in to continue (username `test`, password `test`).")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
cols = st.columns(4)
with cols[0]:
    login = st.button("Log in", type="primary", key="login", disabled=username == "" or password == "")
with cols[1]:
    guest = st.button("Continue as guest", type="secondary", key="guest", disabled=username != "" or password != "")

if login:
    if username == "test" and password == "test":
        with st.spinner("Checking credentials..."):
            st.session_state.authentication_status = True
            st.session_state.username = username
            sleep(1.5)
        with st.spinner("Logged in successfully!"):
            sleep(1.5)
        st.switch_page("pages/Products.py")
    else:
        with st.spinner("Checking credentials..."):
            sleep(2)
        st.error("Incorrect username or password")

if guest:
    with st.spinner("Redirecting to products page..."):
        st.session_state.authentication_status = True
        st.session_state.username = "guest"
        sleep(1.5)
    st.switch_page("pages/Products.py")
