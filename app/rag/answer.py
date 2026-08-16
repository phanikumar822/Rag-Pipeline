from app.rag.retriever import retriever
from app.rag.llm import llms


def answer_question(question:str):
    documents=retriever.invoke(question)

    context="\n\n".join(
        i.page_content for i in documents
    )
    prompt=f"""
Answer the question using only the context below

context :-
{context}

question :-
{question}





"""
    response=llms.invoke(prompt)
    print("DOCUMENTS:", documents)
    print("DOCUMENT COUNT:", len(documents))
    sources=[
        {
            "source":document.metadata.get("source"),
            "page":document.metadata.get("page")
        }
        for document in documents
    ]
    print("SOURCES:", sources)
    print("SOURCE COUNT:", len(sources))

    return {
        "answer":response.content,
        "source":sources
    }