# Stub RxNorm lookup
rx_map = {
    "Metformin": "860975",
    "Lisinopril": "861008"
}

def lookup_rxnorm(med: str) -> str:
    return rx_map.get(med, "Unknown")