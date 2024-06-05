import os

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
DATABASE_URL = f"mongodb://{MONGO_HOST}:27017/"
DATABASE_NAME = "shein"
COLLECTION_URLS = "product_urls"
COLLECTION_DETAILS = "product_details"
COLLECTION_REVIEWS = "product_reviews"
ROW_SIZE = 5

FOOTER = """
<style>
a:link , a:visited{
    color: #4169E1;
    background-color: transparent;
    text-decoration: none;
}

a:hover,  a:active {
    color: #4169E1;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(255,255,255,0.8);
    color: black;
    text-align: center;
    border-top: 1px solid  #7F7F7F;
    border-bottom: 1px solid  #7F7F7F;
}
small {
  font-size: 16px;
  color: #C0C0C0;
  display: inline;
}
</style>
<div class="footer">
<small>Developed with ❤️ by
<a style='display: inline; text-align: center;' href="https://uribealejandro.github.io/"
target="_blank">Alejandro Uribe</a></small>
</div>
"""
