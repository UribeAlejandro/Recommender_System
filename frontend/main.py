import asyncio
from time import sleep

import streamlit as st

from frontend.constants import FOOTER
from frontend.utils.config import make_sidebar


async def main() -> None:
    """Streamlit application entry point."""
    st.set_page_config(
        layout="centered",
        page_icon=":feet:",
        page_title="Home",
        initial_sidebar_state="expanded",
    )

    make_sidebar()
    st.markdown(
        "<h1>"
        '<img src="https://tung-local.myshopify.com/cdn/shop/products/Doge_1024x1024.png?v=1475122208" '
        'style="height:50px;">Doge Market</h1>',
        unsafe_allow_html=True,
    )
    if not st.session_state.get("authentication_status", False):
        with st.container(border=True):
            st.write("Please log in to continue (username `test` should work.")
            st.info("You can also continue as a guest.")
            username = st.text_input("👤 :blue[**Username**]", help="Type your username")
            password = st.text_input(  # noqa
                "🔑 :red[**Password**]",
                type="password",
                help="Type your password",
                placeholder="Passwords are not stored, so feel free to type anything!",
            )
            cols = st.columns(4)
            with cols[0]:
                login = st.button("Log in", type="primary", key="login", disabled=username == "")
            with cols[3]:
                guest = st.button("Continue as guest", type="primary", key="guest", disabled=username != "")

            if login:
                if username != "guest":
                    with st.spinner("Checking credentials..."):
                        st.session_state["authentication_status"] = True
                        st.session_state["username"] = username
                        # sleep(1)
                    st.switch_page("pages/Hot_Products.py")
                else:
                    with st.spinner("Checking credentials..."):
                        sleep(2)
                    st.error("Incorrect username or password")

        if guest:
            with st.spinner("Redirecting to products page..."):
                st.session_state["authentication_status"] = True
                st.session_state["username"] = "guest"
            st.switch_page("pages/Hot_Products.py")
    else:
        with st.spinner("Redirecting to products page..."):
            st.switch_page("pages/Hot_Products.py")

    st.markdown(FOOTER, unsafe_allow_html=True)


if __name__ == "__main__":
    asyncio.run(main())
