import streamlit as st
from streamlit_server_state import server_state

from web.utils.pages import make_sidebar

st.set_page_config(
    layout="wide",
    page_icon=":feet:",
    page_title="Products",
    initial_sidebar_state="collapsed",
)

make_sidebar()
st.title(f"Welcome, {server_state.username}!")

if not server_state["username"] == "guest":
    st.write("Here are some products you might like.")
    # Logic for collaborative filtering
else:
    st.write("Consider creating an account to improve the recommendations!")
    # Logic for content based
