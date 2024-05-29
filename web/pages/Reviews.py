import base64
from math import ceil

import streamlit as st
from streamlit_card import card
from streamlit_server_state import no_rerun, server_state

from web.constants import COLLECTION_DETAILS, COLLECTION_REVIEWS, DATABASE_NAME, FOOTER
from web.utils.database import get_mongo_database
from web.utils.pages import hide_image_fullscreen, make_sidebar

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
if server_state.get("username", None) is None:
    st.warning("Please log in to view your reviews.")
else:
    db = get_mongo_database(DATABASE_NAME)
    collection_reviews = db.get_collection(COLLECTION_REVIEWS)
    collection_products = db.get_collection(COLLECTION_DETAILS)

    reviews = list(collection_reviews.find({"nickname": server_state.username}).sort({"timestamp": -1}))

    ROW_SIZE = 1
    batch_size = 5
    grid = st.columns(ROW_SIZE)
    page = st.session_state.get("page_reviews", 1)
    if page is None:
        st.write("No reviews yet. Go and find the products you love!")
        st.stop()
    num_batches = ceil(len(reviews) / batch_size)
    batch = reviews[(page - 1) * batch_size : page * batch_size]

    if len(reviews) > 0:
        col = 0
        for review in batch:
            _id_review = review["_id"]
            product_id = review["product_id"]
            product_details = collection_products.find_one({"product_id": product_id})
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
                                st.session_state["_id"] = _id_product
                            st.switch_page("pages/Product.py")
                    with rev_cols[1]:
                        st.html(f"<strong>{title}</strong>")
                        st.write(s)
                        st.html(f"<p><strong>\"{review['review']}\"</strong><em> on {review['date']}</em></p>")
                    with rev_cols[2]:
                        delete = st.button("❌", key=f"delete{str(_id_review)}", help="Delete review")
                        if delete:
                            collection_reviews.delete_one({"_id": _id_review})
                            st.rerun()
            col = (col + 1) % ROW_SIZE
    else:
        st.write("No reviews yet. Go and find the products you love!")

    bottom = st.columns([10, 3, 10])
    with bottom[1]:
        page_select = st.selectbox(
            "Page Number", range(1, num_batches + 1), key="page_reviews", disabled=num_batches == 1
        )
st.markdown(FOOTER, unsafe_allow_html=True)
