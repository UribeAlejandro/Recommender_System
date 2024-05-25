import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

from web.utils.auth import logout


@st.cache_data
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


@st.cache_data
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
    with st.sidebar:
        st.title(":dog: Doge Market :dog:")
        st.write("")
        st.write("")

        if st.session_state.get("authentication_status", False):
            st.page_link("pages/Products.py", label="Products", icon="🕵️")
            st.page_link("pages/Top_Picks.py", label="Top Picks for you", icon="🔒")

            if st.session_state.get("username", "guest") != "guest":
                st.write("")
                st.write("")

                if st.button("Log out"):
                    logout()

        elif get_current_page_name() != "main":
            st.switch_page("main.py")
