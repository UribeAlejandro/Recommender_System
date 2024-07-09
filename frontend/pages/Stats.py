import plotly
import streamlit as st

from frontend.constants import FOOTER
from frontend.utils.config import hide_image_fullscreen, make_sidebar
from frontend.utils.controller import get_rating_charts

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


charts = get_rating_charts()

rating_distribution = charts["rating_distribution"]
fig = plotly.io.from_json(rating_distribution)
st.plotly_chart(fig, use_container_width=True)

# rating_distribution_price = charts["rating_distribution_price"]
# fig = plotly.io.from_json(rating_distribution_price)
# st.plotly_chart(fig, use_container_width=True)


# Plot!
# st.plotly_chart(fig, use_container_width=True)
st.markdown(FOOTER, unsafe_allow_html=True)
