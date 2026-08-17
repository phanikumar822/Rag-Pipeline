import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def normalize_groq_base_url(base_url):
    if not base_url:
        return "https://api.groq.com"
    return base_url.rstrip("/").replace("/openai/v1", "")


def get_groq_model_name():
    return os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def get_groq_base_url():
    return normalize_groq_base_url(os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"))


def build_llm(model_name=None, api_key=None, base_url=None, temperature=0.1):
    groq_base_url = normalize_groq_base_url(base_url or get_groq_base_url())
    return ChatGroq(
        model=model_name or get_groq_model_name(),
        api_key=api_key or os.getenv("GROQ_API_KEY"),
        base_url=groq_base_url,
        temperature=temperature,
    )


llms = build_llm()