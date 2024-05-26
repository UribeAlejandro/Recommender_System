import streamlit as st

from web.constants import FOOTER
from web.utils.pages import make_sidebar

st.set_page_config(
    layout="centered",
    page_icon=":feet:",
    page_title="Hot Products",
    initial_sidebar_state="auto",
)
make_sidebar()

st.markdown(
    """
    # Acerca de este sitio

    Este sitio es el proyecto final de la asignatura de **Sistemas de Recomendación** de la
    **Maestría en Minería de Datos & Descubrimiento del Conocimiento** de la **Universidad de Buenos Aires**.

    Desarrollada por: Alejandro Uribe
    """
)

st.markdown(FOOTER, unsafe_allow_html=True)
