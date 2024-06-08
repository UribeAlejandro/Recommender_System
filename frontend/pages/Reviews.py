import base64
from math import ceil

import streamlit as st
from streamlit_card import card
from streamlit_modal import Modal
from streamlit_server_state import no_rerun, server_state

from frontend.constants import BATCH_SIZE_REVIEWS, FOOTER, ROW_SIZE_REVIEWS
from frontend.pages.config import hide_image_fullscreen, make_sidebar
from frontend.utils.backend import delete_review, get_product, get_user_reviews

st.set_page_config(
    layout="centered",
    page_icon="📝",
    page_title="Reviews",
    initial_sidebar_state="collapsed",
)
make_sidebar()
hide_image_fullscreen()

st.header("📝 Reviews")
st.subheader("Your reviews", divider=True)

page = st.session_state.get("page_reviews", 1)

if server_state.get("username", None) is None:
    st.warning("Please log in to view your reviews.")
else:
    grid = st.columns(ROW_SIZE_REVIEWS)
    reviews = get_user_reviews(server_state.username)
    if page is None:
        st.info("No reviews yet. Go and find the products you love!")
        st.stop()
    num_batches = ceil(len(reviews) / BATCH_SIZE_REVIEWS)
    batch = reviews[(page - 1) * BATCH_SIZE_REVIEWS : page * BATCH_SIZE_REVIEWS]

    if len(reviews) > 0:
        col = 0
        for review in batch:
            _id_review = review["_id"]
            product_id = review["product_id"]
            product_details = get_product({"product_id": product_id})
            title = product_details["title"]
            img_route = product_details["image_path"]
            _id_product = product_details["_id"]
            with grid[col]:
                with st.container(border=True):
                    rev_cols = st.columns([2, 4, 1], gap="small")
                    s = ":star:" * review["rating"]
                    with rev_cols[0]:
                        with open(img_route, "rb") as f:
                            data = f.read()
                            encoded = base64.b64encode(data)
                        data = "data:image/png;base64," + encoded.decode("utf-8")
                        product_card = card(
                            title="",
                            text="",
                            image=data,
                            key=str(_id_review),
                            styles={
                                "card": {
                                    "width": "100%",
                                    "height": "180px",
                                    "margin": "5%",
                                    "box-shadow": "0 0 15px rgba(0,0,0,0.5)",
                                    "display": "flex",
                                    "justify-content": "center",
                                },
                                "text": {"position": "absolute", "bottom": -100, "left": 0, "color": "black"},
                                "filter": {"background-color": "rgba(0, 0, 0, 0)"},
                            },
                        )
                        if product_card:
                            with no_rerun:
                                st.session_state["_id"] = str(_id_product)
                            st.switch_page("pages/Product.py")
                    with rev_cols[1]:
                        st.html(f"<strong>{title}</strong>")
                        st.write(s)
                        st.html(f"<p><strong>\"{review['review']}\"</strong><em> on {review['date']}</em></p>")
                    with rev_cols[2]:
                        delete = st.button("❌", key=f"delete{str(_id_review)}", help="Delete review")

                    confirm_delete = Modal(
                        "Are you sure you want to delete this review?", key="modal-delete-review", max_width=450
                    )
                    if delete:
                        confirm_delete.open()
                    if confirm_delete.is_open():
                        with confirm_delete.container():
                            st.write("*This action cannot be undone.*")
                            confirm_cols = st.columns(3)
                            with confirm_cols[0]:
                                cancel = st.button("Cancel", key=f"cancel-delete{str(_id_review)}")
                            with confirm_cols[1]:
                                delete = st.button("Delete", key=f"accept-delete{str(_id_review)}", type="primary")
                            if cancel:
                                confirm_delete.close()
                            if delete:
                                r = delete_review(_id_review, product_id, server_state.username)
                                if r.status_code == 200:
                                    st.success("Review deleted successfully.")
                                    confirm_delete.close()
                                else:
                                    st.error("Failed to delete review.")

            col = (col + 1) % ROW_SIZE_REVIEWS
    else:
        st.info("No reviews yet. Go and find the products you love!")

    bottom = st.columns([10, 3, 10])
    with bottom[1]:
        page_select = st.selectbox(
            "Page Number", range(1, num_batches + 1), key="page_reviews", disabled=num_batches == 1
        )
st.markdown(FOOTER, unsafe_allow_html=True)
