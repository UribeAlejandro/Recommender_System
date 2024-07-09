import base64

import streamlit as st
from streamlit_card import card

from frontend.constants import FOOTER, ROW_SIZE
from frontend.utils.config import hide_image_fullscreen, make_sidebar
from frontend.utils.controller import get_recommendations

st.set_page_config(
    layout="wide",
    page_icon="🔥",
    page_title="Hot Products",
    initial_sidebar_state="collapsed",
)
make_sidebar()
hide_image_fullscreen()

st.header("🔥 Hot Products 🔥")
st.subheader("Products picked for you!", divider=True)

username = st.session_state.get("username", "guest")

with st.spinner("Loading the product list..."):
    products_json = get_recommendations(username)

    number = products_json["number"]
    products = products_json["items"]
    model_name = products_json["model"]

    if number == 0:
        st.error("No products found.")
        st.stop()

    st.success(
        f"Hello **{st.session_state.get("username")}**! We have {number} recommended products for your pet! 🐶🐱🐹🐰🐦🐢🐍🐠🦎🐾🦜🐴🐷🐄🐑🐓🦃🦢🦆🦉🦚🦜🦇🦋🐝🐞🦗🕷🦟🦠"  # noqa
    )
    st.markdown(f"**Model**: {model_name}")

    grid = st.columns(ROW_SIZE)

    col = 0
    for product in products:
        with grid[col]:
            _id = product["_id"]
            title = product["title"]
            img_route = product["image_path"]
            price_discount = product["price_discount"]
            price_real = product.get("price_real")
            off_percent = product.get("off_percent", 0)
            __off_percent = f"{off_percent}% off" if off_percent else ""

            with open(img_route, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data)
            data = "data:image/png;base64," + encoded.decode("utf-8")

            with st.container(height=370):
                product_card = card(
                    title=f"{__off_percent}",
                    text=f"${price_discount}",
                    image=data,
                    key=str(_id),
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "180px",
                            "margin": "0%",
                            "box-shadow": "0 0 5px rgba(0,0,0,0.5)",
                            "display": "inline-flex",
                            "justify-content": "center",
                        },
                        "text": {"position": "absolute", "bottom": 0, "left": 50, "color": "green"},
                        "title": {"position": "absolute", "bottom": 120, "right": 15, "color": "red"},
                        "filter": {"background-color": "rgba(0, 0, 0, 0)"},
                    },
                )
                st.write(title[0:90])

                if product_card:
                    st.session_state["_id"] = _id
                    st.switch_page("pages/Product.py")

        col = (col + 1) % ROW_SIZE
    st.divider()
st.markdown(FOOTER, unsafe_allow_html=True)
