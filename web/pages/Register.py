import streamlit as st
from streamlit_server_state import server_state

from web.utils.pages import make_sidebar

st.set_page_config(
    layout="centered",
    page_icon=":feet:",
    page_title="Register",
    initial_sidebar_state="collapsed",
)
make_sidebar()

st.write(server_state.get("name", "F"))
