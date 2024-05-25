import streamlit as st

from web.utils.pages import make_sidebar

st.set_page_config(
    layout="wide",
    page_icon=":feet:",
    page_title="Products",
    initial_sidebar_state="collapsed",
)

make_sidebar()
