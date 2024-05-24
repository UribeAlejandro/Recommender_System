import time

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from web.utils.auth import config_auth, login_guest

st.set_page_config(page_title="Products", layout="centered", page_icon="👋", initial_sidebar_state="collapsed")

authenticator = config_auth()

authenticator.login()

if st.session_state["authentication_status"] or st.button("Continue as a guest", on_click=login_guest):
    with st.spinner("Loading..."):
        time.sleep(2)
    authenticator.logout(location="sidebar")
    switch_page("Products")
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
