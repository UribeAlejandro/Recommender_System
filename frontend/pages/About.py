import streamlit as st

from frontend.constants import FOOTER
from frontend.utils.config import make_sidebar

st.set_page_config(
    layout="centered",
    page_icon="ℹ️",
    page_title="About",
    initial_sidebar_state="collapsed",
)
make_sidebar()

with open("README.html") as f:
    st.html(f.read())


st.markdown(FOOTER, unsafe_allow_html=True)
