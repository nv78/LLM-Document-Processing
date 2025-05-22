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
git clone LLM-Document-Processing
cd LLM-Document-Processing

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

### Output From test_all.py

```
 python3 test_all.py

=== Document 1: Sample Note ===
Extract status: 200
Structured: {
  "patient_name": "John Doe",
  "birth_date": "1985-03-14",
  "gender": "Male",
  "conditions": [
    "Headache",
    "Hypertension"
  ],
  "medications": [
    "Acetaminophen",
    "Lisinopril"
  ],
  "condition_codes": {
    "Headache": "Unknown",
    "Hypertension": "I10"
  },
  "medication_codes": {
    "Acetaminophen": "Unknown",
    "Lisinopril": "861008"
  }
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": "John Doe"
      }
    ],
    "gender": "Male",
    "birthDate": "1985-03-14"
  },
  "conditions": [
    {
      "resourceType": "Condition",
      "id": "1",
      "subject": {
        "reference": "Patient/1"
      },
      "code": {
        "text": "Headache"
      },
      "clinicalStatus": "active",
      "verificationStatus": "confirmed"
    },
    {
      "resourceType": "Condition",
      "id": "2",
      "subject": {
        "reference": "Patient/1"
      },
      "code": {
        "text": "Hypertension"
      },
      "clinicalStatus": "active",
      "verificationStatus": "confirmed"
    }
  ],
  "medications": [
    {
      "resourceType": "MedicationStatement",
      "id": "1",
      "subject": {
        "reference": "Patient/1"
      },
      "medicationCodeableConcept": {
        "text": "Acetaminophen"
      },
      "status": "active"
    },
    {
      "resourceType": "MedicationStatement",
      "id": "2",
      "subject": {
        "reference": "Patient/1"
      },
      "medicationCodeableConcept": {
        "text": "Lisinopril"
      },
      "status": "active"
    }
  ]
}

=== Document 2: soap_01.txt ===
Extract status: 200
Structured: {
  "error": "Invalid request",
  "condition_codes": {},
  "medication_codes": {}
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": null
      }
    ],
    "gender": null,
    "birthDate": null
  },
  "conditions": [],
  "medications": []
}

=== Document 3: soap_02.txt ===
Extract status: 200
Structured: {
  "error": "Invalid request",
  "condition_codes": {},
  "medication_codes": {}
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": null
      }
    ],
    "gender": null,
    "birthDate": null
  },
  "conditions": [],
  "medications": []
}

=== Document 4: soap_03.txt ===
Extract status: 200
Structured: {
  "error": "Invalid request",
  "condition_codes": {},
  "medication_codes": {}
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": null
      }
    ],
    "gender": null,
    "birthDate": null
  },
  "conditions": [],
  "medications": []
}

=== Document 5: soap_04.txt ===
Extract status: 200
Structured: {
  "error": "Invalid request",
  "condition_codes": {},
  "medication_codes": {}
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": null
      }
    ],
    "gender": null,
    "birthDate": null
  },
  "conditions": [],
  "medications": []
}

=== Document 6: soap_05.txt ===
Extract status: 200
Structured: {
  "error": "Invalid request",
  "condition_codes": {},
  "medication_codes": {}
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": null
      }
    ],
    "gender": null,
    "birthDate": null
  },
  "conditions": [],
  "medications": []
}

=== Document 7: soap_06.txt ===
Extract status: 200
Structured: {
  "error": "Invalid request",
  "condition_codes": {},
  "medication_codes": {}
}
FHIR status: 200
FHIR: {
  "patient": {
    "resourceType": "Patient",
    "id": "1",
    "name": [
      {
        "text": null
      }
    ],
    "gender": null,
    "birthDate": null
  },
  "conditions": [],
  "medications": []
}

--- RAG Test Doc 1: "What did the patient report subjectively?" ---
Status: 200
Answer: The patient reported a headache.
Source doc: 1

--- RAG Test Doc 2: "What was the clinician's assessment?" ---
Status: 200
Answer: The clinician's assessment was that the patient likely had a tension headache due to stress or muscle tension, and recommended pain medication and stress management techniques.
Source doc: 1

--- RAG Test Doc 3: "List any medications mentioned." ---
Status: 200
Answer: 1. Ibuprofen
2. Tylenol
3. Excedrin
Source doc: 1
```

### Output from Docker Compose Logs
```
docker-compose logs -f app
Attaching to llm-document-processing_app_1
app_1  | INFO:     Started server process [1]
app_1  | INFO:     Waiting for application startup.
app_1  | INFO:     Application startup complete.
app_1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
app_1  | INFO:     172.22.0.1:62304 - "GET /documents HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62306 - "POST /extract_structured HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62310 - "POST /to_fhir HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62312 - "POST /extract_structured HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62314 - "POST /to_fhir HTTP/1.1" 200 OK
...
app_1  | INFO:     172.22.0.1:62394 - "POST /to_fhir HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62396 - "POST /extract_structured HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62398 - "POST /to_fhir HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62400 - "GET /documents HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62402 - "POST /answer_question HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62404 - "POST /answer_question HTTP/1.1" 200 OK
app_1  | INFO:     172.22.0.1:62406 - "POST /answer_question HTTP/1.1" 200 OK
```
