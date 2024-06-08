import plotly
import plotly.express as px
import streamlit as st

from frontend.constants import FOOTER
from frontend.pages.config import hide_image_fullscreen, make_sidebar

st.set_page_config(
    layout="centered",
    page_icon="📝",
    page_title="Reviews",
    initial_sidebar_state="collapsed",
)
make_sidebar()
hide_image_fullscreen()

st.header("📊 Stats")
st.subheader("Stats", divider=True)

st.write("This is a simple example of a distribution plot.")
fig = px.histogram(x=range(10), y=range(10))

html = fig.to_json()

fig = plotly.io.from_json(html)
# .read_json(html)

st.plotly_chart(fig, use_container_width=True)


# Plot!
st.plotly_chart(fig, use_container_width=True)
st.markdown(FOOTER, unsafe_allow_html=True)
