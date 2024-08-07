import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

from frontend.utils.auth import logout


def hide_image_fullscreen():
    """Hides the fullscreen button in the Streamlit app."""
    st.markdown(
        """<style>
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
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = False
    with st.sidebar:
        st.markdown(
            """
            <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    margin-top: 2rem;
                }
                .reportview-container {
                    margin-top: -2em;
                }
                #MainMenu {visibility: hidden;}
                .stDeployButton {display:none;}
                footer {visibility: hidden;}
                #stDecoration {display:none;}
            </style>
            <h1><img
            src="https://tung-local.myshopify.com/cdn/shop/products/Doge_1024x1024.png?v=1475122208"
            style="height:50px;">Doge Market</h1>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<h1>Navigation 🚀</h1>", unsafe_allow_html=True)
        st.markdown("<h3>Home 🏠</h3>", unsafe_allow_html=True)
        st.page_link(icon="🏠", page="main.py", label="Home", disabled=False)

        if st.session_state.get("authentication_status", False):
            st.markdown("<h3>Products 📒</h3>", unsafe_allow_html=True)
            st.page_link(
                icon="🎁",
                page="pages/Products.py",
                label="Products List",
                disabled=False,
                # disabled=not server_state.get("authentication_status", False),
            )
            st.page_link(
                icon="🔥",
                page="pages/Hot_Products.py",
                label="Hot Products",
                disabled=not st.session_state.get("authentication_status", True),
            )
            st.markdown("<h3>Reviews 📝</h3>", unsafe_allow_html=True)
            st.page_link(icon="📝", page="pages/Reviews.py", label="Reviews", disabled=False)
            st.markdown("<h3>Stats 📊</h3>", unsafe_allow_html=True)
            st.page_link(icon="📊", page="pages/Stats.py", label="Stats", disabled=False)

            if st.session_state.get("username", "guest") != "guest":
                if st.button("Log out", type="primary"):
                    logout()
        elif get_current_page_name() == "About":
            pass
        elif get_current_page_name() != "main":
            st.switch_page("main.py")
