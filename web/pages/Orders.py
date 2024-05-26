import streamlit as st

from web.constants import FOOTER
from web.utils.pages import get_current_page_name, make_sidebar

st.set_page_config(
    layout="centered",
    page_icon=":feet:",
    page_title="Hot Products",
    initial_sidebar_state="auto",
)
make_sidebar()


st.header(get_current_page_name())

st.markdown(FOOTER, unsafe_allow_html=True)
