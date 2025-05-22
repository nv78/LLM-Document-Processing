#!/usr/bin/env python3
import requests
from urllib.parse import urlparse, parse_qs, unquote

BASE = "http://localhost:8000"
SOAP_URLS = [
    "https://file.notion.so/f/f/…/soap_01.txt?downloadName=soap_01.txt",
    "https://file.notion.so/f/f/…/soap_02.txt?downloadName=soap_02.txt",
    "https://file.notion.so/f/f/…/soap_03.txt?downloadName=soap_03.txt",
    "https://file.notion.so/f/f/…/soap_04.txt?downloadName=soap_04.txt",
    "https://file.notion.so/f/f/…/soap_05.txt?downloadName=soap_05.txt",
    "https://file.notion.so/f/f/…/soap_06.txt?downloadName=soap_06.txt",
]

def seed_documents():
    print("== Seeding documents ==")
    for url in SOAP_URLS:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"⚠️ Failed to fetch {url}: {r.status_code}")
            continue
        # extract the downloadName param for title
        q = parse_qs(urlparse(url).query)
        title = unquote(q.get("downloadName", ["untitled"])[0])
        payload = {"title": title, "content": r.text}
        resp = requests.post(f"{BASE}/documents", json=payload)
        if resp.status_code == 200:
            print(f"✔ Seeded {title} → id={resp.json()['id']}")
        else:
            print(f"✘ Failed to seed {title}: [{resp.status_code}] {resp.text}")

def test_extraction_and_fhir():
    print("\n== Testing extraction and FHIR ==")
    docs = requests.get(f"{BASE}/documents").json()
    for d in docs:
        print(f"\n--- Document {d['id']}: {d['title']} ---")
        # 1) extract structured
        r1 = requests.post(f"{BASE}/extract_structured", json={"text": d["content"]})
        print("Extract status:", r1.status_code)
        try:
            structured = r1.json().get("structured")
            print("Structured:", structured)
        except ValueError:
            print("❌ Extraction returned non-JSON:", r1.text)
            continue

        # 2) convert to FHIR
        r2 = requests.post(f"{BASE}/to_fhir", json={"structured": structured})
        print("FHIR status:", r2.status_code)
        try:
            print("FHIR:", r2.json())
        except ValueError:
            print("❌ FHIR returned non-JSON:", r2.text)

if __name__ == "__main__":
    seed_documents()
    test_extraction_and_fhir()
