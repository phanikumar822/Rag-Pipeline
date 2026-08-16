from fastapi import APIRouter
from app.models.chat import ChatRequest

from app.rag.answer import answer_question

router=APIRouter()


@router.post("/chat")
def chat(request:ChatRequest):
    answer=answer_question(
        request.question
    )
    return {
        "question":request.question,
        "answer":answer["answer"],
        "source":answer["source"]
    }