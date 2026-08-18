from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os

def get_qdrant_url():
    return os.getenv("QDRANT_URL", "http://localhost:6333")

clients = QdrantClient(
    url=get_qdrant_url(),
    api_key=os.getenv("QDRANT_API_KEY", None)
)

if not clients.collection_exists("production-rag-v3"):
    clients.create_collection(
        collection_name="production-rag-v3",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

embedding_model = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)

vector_db = QdrantVectorStore(
    client=clients,
    collection_name="production-rag-v3",
    embedding=embedding_model
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)