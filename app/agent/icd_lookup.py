# Stub ICD lookup
icd_map = {
    "Type 2 Diabetes Mellitus": "E11",
    "Hypertension": "I10"
}

def lookup_icd(condition: str) -> str:
    return icd_map.get(condition, "Unknown")