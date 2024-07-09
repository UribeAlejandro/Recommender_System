import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = "shein-mirror"
COLLECTION_DETAILS = "product_details"
COLLECTION_REVIEWS = "product_reviews"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://database:27017")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2.gguf2.f16.gguf"
