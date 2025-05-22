# Medical Document Processor

A FastAPI backend that demonstrates:

1. Database-backed document storage (Part 1)
2. LLM integration for summarization and Q&A (Part 2 & 3)
3. Retrieval-Augmented Generation pipeline (Part 3)
4. Agent-based structured data extraction with ICD/RxNorm coding (Part 4)
5. Conversion to simplified FHIR resources (Part 5)
6. Containerization and orchestration with Docker Compose (Part 6)

## Setup

```bash
# Clone repo
git clone <repo-url>
cd medical-doc-processor

# Copy env file
cp .env.example .env
# Edit .env to add OPENAI_API_KEY, DATABASE_URL, etc.

# Build and run all services
docker-compose up --build -d

# Seed the database (optional)
bash init_data.sh
```

## Endpoints

| Endpoint                | Method | Description                            |
|-------------------------|--------|----------------------------------------|
| `/health`               | GET    | Health check                           |
| `/documents`            | GET    | List documents                         |
| `/documents`            | POST   | Add a new document                     |
| `/summarize_note`       | POST   | LLM-based summary                      |
| `/answer_question`      | POST   | RAG-based question answering           |
| `/extract_structured`   | POST   | Agent-based structured extraction      |
| `/to_fhir`              | POST   | Convert structured data to FHIR format |