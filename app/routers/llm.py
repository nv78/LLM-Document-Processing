from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.llm_client import summarize_text, generate_answer
from app.rag.store import store

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

@router.post("/summarize_note", response_model=SummarizeResponse)
def summarize_note(req: SummarizeRequest):
    summary = summarize_text(req.text)
    return SummarizeResponse(summary=summary)

class QARequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    answer: str
    source_doc_id: int

@router.post("/answer_question", response_model=QAResponse)
def answer_question(req: QARequest):
    results = store.query(req.question, top_k=1)
    doc_id, _, text = results[0]
    answer = generate_answer(req.question, text)
    return QAResponse(answer=answer, source_doc_id=doc_id)