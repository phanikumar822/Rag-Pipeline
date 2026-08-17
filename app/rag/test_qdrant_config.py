from app.rag.embeddings import get_qdrant_url


def test_default_qdrant_url_uses_localhost():
    assert get_qdrant_url() == "http://localhost:6333"
