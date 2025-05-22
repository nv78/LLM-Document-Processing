from fastapi import FastAPI
from app.db import engine, SessionLocal
from app.models import Base
from app.routers import health, docs, llm, extract, fhir
from app.rag.store import store

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(health.router)
app.include_router(docs.router)
app.include_router(llm.router)
app.include_router(extract.router)
app.include_router(fhir.router)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    from app.models import Document
    docs = db.query(Document).all()
    for d in docs:
        store.add(d.id, d.content)
    db.close()