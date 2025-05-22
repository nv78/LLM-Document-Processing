#!/usr/bin/env python3
import requests
import json

BASE = "http://localhost:8000"

def test_extraction_and_fhir():
    docs = requests.get(f"{BASE}/documents").json()

    for d in docs:
        print(f"\n=== Document {d['id']}: {d['title']} ===")

        # 1) Extract structured
        r1 = requests.post(
            f"{BASE}/extract_structured",
            json={"text": d["content"]},
        )
        print("Extract status:", r1.status_code)
        try:
            structured = r1.json().get("structured")
            print("Structured:", json.dumps(structured, indent=2))
        except Exception:
            print("❌ Extraction returned non-JSON:", r1.text)
            continue

        # 2) Convert to FHIR
        r2 = requests.post(
            f"{BASE}/to_fhir",
            json={"structured": structured},
        )
        print("FHIR status:", r2.status_code)
        try:
            print("FHIR:", json.dumps(r2.json(), indent=2))
        except Exception:
            print("❌ FHIR returned non-JSON:", r2.text)


def test_rag():
    """
    For each document, ask a simple question that should
    be answerable from its content. We assert we get back
    a non-empty answer and the source_doc_id matches one
    of our known IDs.
    """
    docs = requests.get(f"{BASE}/documents").json()
    doc_ids = {d["id"] for d in docs}

    # Example questions mapping: document id -> question
    # Tailor these to your actual SOAP notes!
    QUESTIONS = {
        1: "What did the patient report subjectively?",
        2: "What was the clinician's assessment?",
        3: "List any medications mentioned.",
        # add more mappings for docs 4,5,6 if you like
    }

    for doc_id, question in QUESTIONS.items():
        print(f"\n--- RAG Test Doc {doc_id}: \"{question}\" ---")
        resp = requests.post(
            f"{BASE}/answer_question",
            json={"question": question}
        )
        print("Status:", resp.status_code)
        if resp.status_code != 200:
            print("❌ Failed to get an answer:", resp.text)
            continue

        data = resp.json()
        answer = data.get("answer", "")
        source = data.get("source_doc_id")
        print("Answer:", answer)
        print("Source doc:", source)

        # Basic sanity checks
        assert source in doc_ids, f"Unknown source_doc_id {source}"
        assert answer and len(answer) > 5, "Answer too short"


if __name__ == "__main__":
    # assuming you've already run seed_local.sh and your service is up
    test_extraction_and_fhir()
    test_rag()
