from app.rag.llm import normalize_groq_base_url


def test_groq_base_url_removes_openai_v1_suffix():
    assert normalize_groq_base_url("https://api.groq.com/openai/v1") == "https://api.groq.com"


if __name__ == "__main__":
    test_groq_base_url_removes_openai_v1_suffix()
    print("test_groq_base_url_removes_openai_v1_suffix: PASS")
