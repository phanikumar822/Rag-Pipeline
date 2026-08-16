from app.rag.embeddings import retriever
from app.rag.reranker import rerank_document

question = "explain getting started exercises"

documents = retriever.invoke(question)

best_documents = rerank_document(
    question,
    documents,
    top_k=3
)

for document in best_documents:

    print(document.page_content)
    print(document.metadata)
    print("--------------------")