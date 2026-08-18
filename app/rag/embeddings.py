from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os


# -----------------------------
# Qdrant Configuration
# -----------------------------

def get_qdrant_url():
    return os.getenv(
        "QDRANT_URL",
        "http://localhost:6333"
    )


QDRANT_COLLECTION = "production-rag-v3"


# -----------------------------
# Qdrant Client
# -----------------------------

client = QdrantClient(
    url=get_qdrant_url(),
    api_key=os.getenv("QDRANT_API_KEY")
)


# -----------------------------
# Create Collection if Needed
# -----------------------------

if not client.collection_exists(QDRANT_COLLECTION):
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


# -----------------------------
# HuggingFace Embeddings
# -----------------------------

embedding_model = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)


# -----------------------------
# Qdrant Vector Store
# -----------------------------

vector_db = QdrantVectorStore(
    client=client,
    collection_name=QDRANT_COLLECTION,
    embedding=embedding_model
)


# -----------------------------
# Retriever
# -----------------------------

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 3
    }
)