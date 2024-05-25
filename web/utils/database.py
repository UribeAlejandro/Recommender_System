from os import listdir

import streamlit as st

from web.constants import IMG_DIRECTORY


@st.cache_data
def get_files():
    """
    Get the files in the image directory.

    Returns
    -------
    list
        The list of files.
    """
    files = listdir(IMG_DIRECTORY)
    return files
