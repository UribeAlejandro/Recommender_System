import os

from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 400
TOTAL_ROWS = 10000

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

EMBEDDINGS_MODEL = "all-MiniLM-L6-v2.gguf2.f16.gguf"
