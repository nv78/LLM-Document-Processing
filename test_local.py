#!/usr/bin/env python3
import glob
import os
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

if __name__ == "__main__":
    # You can optionally reseed here if you like,
    # but assuming you've already run seed_local.sh:

    test_extraction_and_fhir()
