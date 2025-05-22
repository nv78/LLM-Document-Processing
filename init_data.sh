#!/bin/bash
# Seed DB with a sample note
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title":"Sample Note","content":"Subjective: Patient reports headache..."}'