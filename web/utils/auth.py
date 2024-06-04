from time import sleep

import streamlit as st
from streamlit_server_state import no_rerun, server_state


def logout():
    """Logs out the user and redirects to the main page."""
    with st.spinner("Redirecting..."):
        with no_rerun:
            server_state.authentication_status = False
            server_state.username = None
        sleep(0.5)
    st.info("Logged out successfully!")
    st.switch_page("main.py")
