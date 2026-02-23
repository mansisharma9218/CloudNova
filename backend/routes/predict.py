from fastapi import APIRouter, Depends
from auth import verify_token

router = APIRouter()

def calculate_base_cost(vcpu, ram_gb, storage_gb, usage_hours):
    return vcpu * 8 + ram_gb * 3.5 + storage_gb * 0.08 + (usage_hours / 720) * 12


@router.post("/")
def predict_cost(
    vcpu: int,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    user = Depends(verify_token)
):
    base = calculate_base_cost(vcpu, ram_gb, storage_gb, usage_hours)

    return {
        "predicted_monthly_cost_usd": round(base, 2),
        "providers": {
            "AWS": round(base * 1.05, 2),
            "Azure": round(base * 1.02, 2),
            "GCP": round(base * 0.96, 2),
        },
        "recommendation": "GCP",
        "savings_vs_most_expensive": round(base * 1.05 - base * 0.96, 2),
    }