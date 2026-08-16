from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

import os

clients = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://host.docker.internal:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None)
)

if not clients.collection_exists("production-rag"):

    clients.create_collection(
        collection_name="production-rag",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_db = QdrantVectorStore(
    client=clients,
    collection_name="production-rag",
    embedding=embedding_model
)


retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 3
    }
)