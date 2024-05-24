import streamlit as st
import yaml
from streamlit_authenticator import Authenticate
from yaml import SafeLoader


def config_auth() -> Authenticate:
    """
    Load the authentication configuration from the config.yaml file.

    Returns
    -------
    Authenticate: The Authenticate object
    """
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )
    return authenticator


def login_guest() -> None:
    """Log in as a guest."""
    st.session_state["authentication_status"] = True
    st.session_state["name"] = "Guest"
    st.session_state["username"] = "guest"
