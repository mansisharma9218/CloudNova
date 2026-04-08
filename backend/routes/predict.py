from fastapi import APIRouter, Depends
from auth import verify_token
import pickle
import os
from utils.cost_utils import compute_cost

router = APIRouter()

# ─────────────────────────
# Load ML model + encoders
# ─────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "ml_model", "cost_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "..", "ml_model", "encoders.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(ENCODER_PATH, "rb") as f:
    encoders = pickle.load(f)

le_provider = encoders["provider"]
le_region   = encoders["region"]
le_pricing  = encoders["pricing"]


# ─────────────────────────
# Predict endpoint
# ─────────────────────────

@router.post("/")
def predict_cost(
    vcpu: int,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    region: str,
    pricing_model: str,
    user=Depends(verify_token)
):
    providers = ["AWS", "Azure", "GCP"]
    results = {}

    for provider in providers:
        cost = compute_cost(
            model,
            le_provider,
            le_region,
            le_pricing,
            vcpu,
            ram_gb,
            storage_gb,
            usage_hours,
            provider,
            region,
            pricing_model
        )
        results[provider] = cost

    best_provider = min(results, key=results.get)
    worst_provider = max(results, key=results.get)

    return {
        "recommendation": best_provider,
        "predicted_costs": results,
        "savings_vs_most_expensive": round(results[worst_provider] - results[best_provider], 2)
    }