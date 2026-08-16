from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

from app.rag.retriever import retriever
from app.rag.reranker import rerank_document
from app.rag.llm import llms


def retrieve_and_rerank(state: MessagesState):

    question = state["messages"][-1].content

    documents = retriever.invoke(question)

    documents = rerank_document(
        question,
        documents,
        top_k=3
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return {
        "messages": [
            SystemMessage(
                content=f"""
                summarize document explain clearly

Context:
{context}
"""
            )
        ]
    }


def generate(state: MessagesState):

    response = llms.invoke(state["messages"])

    return {
        "messages": [
            response
        ]
    }


graph = StateGraph(MessagesState)

graph.add_node(
    "retrieve",
    retrieve_and_rerank
)

graph.add_node(
    "generate",
    generate
)

graph.add_edge(
    START,
    "retrieve"
)

graph.add_edge(
    "retrieve",
    "generate"
)

graph.add_edge(
    "generate",
    END
)

app = graph.compile()


response = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="What is the annual leave policy?"
            )
        ]
    }
)

print(response["messages"][-1].content)