from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FHIRRequest(BaseModel):
    structured: dict

class FHIRResponse(BaseModel):
    patient: dict
    conditions: list
    medications: list

@router.post("/to_fhir", response_model=FHIRResponse)
def to_fhir(req: FHIRRequest):
    data = req.structured
    patient = {
        "resourceType": "Patient",
        "id": "1",
        "name": [{"text": data.get("patient_name")}],
        "gender": data.get("gender"),
        "birthDate": data.get("birth_date")
    }
    conditions = []
    for i, cond in enumerate(data.get("conditions", []), start=1):
        conditions.append({
            "resourceType": "Condition",
            "id": str(i),
            "subject": {"reference": "Patient/1"},
            "code": {"text": cond},
            "clinicalStatus": "active",
            "verificationStatus": "confirmed"
        })
    medications = []
    for i, med in enumerate(data.get("medications", []), start=1):
        medications.append({
            "resourceType": "MedicationStatement",
            "id": str(i),
            "subject": {"reference": "Patient/1"},
            "medicationCodeableConcept": {"text": med},
            "status": "active"
        })
    return FHIRResponse(patient=patient, conditions=conditions, medications=medications)