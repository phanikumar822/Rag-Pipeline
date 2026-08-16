from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

import os

llms=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)