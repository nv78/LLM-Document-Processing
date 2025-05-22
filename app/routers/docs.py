from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app.models import Document, DocumentCreate, DocumentSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/documents", response_model=List[DocumentSchema])
def read_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.post("/documents", response_model=DocumentSchema)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(title=doc.title, content=doc.content)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc