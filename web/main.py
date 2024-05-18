import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_navigation_bar import st_navbar
from yaml.loader import SafeLoader

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)

page = st_navbar(["Home", "Documentation", "Examples", "Community", "Login"], options={"show_menu": True})
if page == "Login":
    authenticator.login()
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
else:
    st.write(page)
with st.sidebar:
    st.markdown("This is a sidebar")

# if open_modal:


# with st.sidebar:
#

#

#

#
# # def render_web():
#
# #
# # if "logged" not in st.session_state:
# #
# #     st.session_state.logged = True
# #
# # with st.spinner():
# #     alert = st.success("Done!")
# #     time.sleep(5)
# #     alert.empty()
# #

#
#     st.button("Continue as guest")
#
