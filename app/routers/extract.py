from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import openai

from app.config import settings
from app.agent.icd_lookup import lookup_icd
from app.agent.rxnorm_lookup import lookup_rxnorm

openai.api_key = settings.OPENAI_API_KEY
router = APIRouter()

class ExtractRequest(BaseModel):
    text: str

class ExtractResponse(BaseModel):
    structured: dict

@router.post("/extract_structured", response_model=ExtractResponse)
def extract_structured(req: ExtractRequest):
    prompt = f"Extract patient_name, birth_date (YYYY-MM-DD), gender, conditions (list of strings), medications (list of strings) from this medical note and return JSON only. Note: {req.text}"
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    try:
        data = json.loads(resp.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to parse JSON")
    # enrich codes
    data["condition_codes"] = {c: lookup_icd(c) for c in data.get("conditions", [])}
    data["medication_codes"] = {m: lookup_rxnorm(m) for m in data.get("medications", [])}
    return ExtractResponse(structured=data)