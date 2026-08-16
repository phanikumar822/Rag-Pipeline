from app.rag.embeddings import retriever
question="25951A05DK row details"

results=retriever.invoke(question)
