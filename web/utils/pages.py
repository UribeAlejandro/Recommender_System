import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from streamlit_server_state import server_state, server_state_lock

from web.utils.auth import logout


def css():
    """Hides the fullscreen button in the Streamlit app."""
    st.markdown(
        """
        <style>
            button[title = "View fullscreen"]{
                visibility: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_current_page_name():
    """
    Get the name of the current page.

    Returns
    -------
    str
        The name of the current page.
    """
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    """Create the sidebar for the Streamlit app."""
    with server_state_lock["authentication_status"]:
        if "authentication_status" not in server_state:
            server_state.authentication_status = False

    with st.sidebar:
        st.title(":dog: Doge Market :dog:")
        st.write("")
        st.write("")

        if server_state.get("authentication_status", False):
            st.page_link(icon="🕵️", page="pages/Products.py", label="Products")
            st.page_link(icon="🔥", page="pages/Hot_Products.py", label="Hot Products")
            st.page_link(icon="🔥", page="pages/Top_Picks.py", label="Top Picks for you")

            st.write("")
            st.write("")
            st.write("")

            if server_state.get("username", "guest") != "guest":
                if st.button("Log out"):
                    logout()
            else:
                if st.button("Register"):
                    st.switch_page("pages/Register.py")

        elif get_current_page_name() != "main":
            st.switch_page("main.py")
