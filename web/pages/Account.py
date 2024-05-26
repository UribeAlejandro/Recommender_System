import streamlit as st
from streamlit_server_state import server_state

from web.constants import FOOTER
from web.utils.pages import make_sidebar

st.set_page_config(
    layout="centered",
    page_icon=":feet:",
    page_title="Hot Products",
    initial_sidebar_state="auto",
)
make_sidebar()


st.write(server_state.get("name", "F"))


st.markdown(FOOTER, unsafe_allow_html=True)
