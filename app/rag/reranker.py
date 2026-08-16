from sentence_transformers import CrossEncoder

reranking_model=CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_document(
        question,
        documents,
        top_k=3
):

    pairs=[[question,document.page_content]
    for document in documents
    ]

    scores=reranking_model.predict(pairs)

    reranked_documents=sorted(
        zip(scores,documents),
        key=lambda x:x[0],
        reverse=True
    )

    return[
        document
        for score,document in reranked_documents[:top_k]
    ]

    