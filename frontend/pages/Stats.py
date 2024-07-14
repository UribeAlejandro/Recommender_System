import asyncio

import plotly
import streamlit as st

from frontend.constants import FOOTER
from frontend.utils.config import hide_image_fullscreen, make_sidebar


async def stats() -> None:
    """Display the stats page."""
    st.set_page_config(
        layout="wide",
        page_icon="📝",
        page_title="Reviews",
        initial_sidebar_state="collapsed",
    )
    make_sidebar()
    hide_image_fullscreen()

    st.header("📊 Stats", divider=True)

    st.subheader("Rating Distribution", divider=True)
    st.write("The following charts are generated from the data in the database.")

    cols = st.columns(2)

    with cols[0]:
        with open("img/charts/rating_distribution_before_sentiment.json") as f:
            rating_no_sentiment = f.read()

        fig = plotly.io.from_json(rating_no_sentiment)
        st.plotly_chart(fig, use_container_width=True)

    with cols[1]:
        with open("img/charts/rating_distribution_after_sentiment.json") as f:
            rating_sentiment = f.read()

        fig = plotly.io.from_json(rating_sentiment)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Collaborative Filtering", divider=True)
    st.write("The charts below regards the models performance.")

    cols = st.columns([1, 5, 1])
    with cols[1]:
        with open("img/charts/result_metrics.json") as f:
            result_metrics = f.read()
        fig = plotly.io.from_json(result_metrics)
        st.plotly_chart(fig, use_container_width=True)

        with open("img/charts/error_distribution.json") as f:
            error_distribution = f.read()
        fig = plotly.io.from_json(error_distribution)
        st.plotly_chart(fig, use_container_width=True)

        st.warning("The error is calculated as the difference between the predicted rating and the actual rating.")
        st.write("The chart below shows the error distribution of the model.")
        st.write(
            "The eror has a local minimum at `11` products, which means that the model is good at that point. "
            "Thus, this is the minimum number of reviews a user should have to get a good recommendation."
        )
        with open("img/charts/error_vs_number_of_items_rated_by_user.json") as f:
            error_vs_number_of_items_rated_by_user = f.read()
        fig = plotly.io.from_json(error_vs_number_of_items_rated_by_user)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(FOOTER, unsafe_allow_html=True)


asyncio.run(stats())
