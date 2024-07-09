from time import sleep

import streamlit as st


def logout():
    """Logs out the user and redirects to the main page."""
    with st.spinner("Redirecting..."):
        st.session_state["authentication_status"] = False
        st.session_state["username"] = None
        sleep(0.5)
    st.info("Logged out successfully!")
    st.switch_page("main.py")
