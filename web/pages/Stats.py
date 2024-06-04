import streamlit as st

from web.constants import FOOTER
from web.utils.pages import hide_image_fullscreen, make_sidebar

st.set_page_config(
    layout="centered",
    page_icon="📝",
    page_title="Reviews",
    initial_sidebar_state="collapsed",
)
make_sidebar()
hide_image_fullscreen()

st.header("📊 Stats")
st.subheader("Stats", divider=True)


st.markdown(FOOTER, unsafe_allow_html=True)
