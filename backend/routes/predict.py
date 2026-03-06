from fastapi import APIRouter, Depends
from auth import verify_token
import pandas as pd
import pickle
import os

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

        provider_enc = le_provider.transform([provider])[0]
        region_enc = le_region.transform([region])[0]
        pricing_enc = le_pricing.transform([pricing_model])[0]

        base_price = (vcpu * 0.045) + (ram_gb * 0.006)
        monthly_estimate = base_price * usage_hours
        price_per_vcpu = monthly_estimate / vcpu

        input_df = pd.DataFrame([{
            "vcpu": vcpu,
            "ram_gb": ram_gb,
            "storage_gb": storage_gb,
            "usage_hours": usage_hours,
            "price_per_vcpu": price_per_vcpu,
            "provider_enc": provider_enc,
            "region_enc": region_enc,
            "pricing_model_enc": pricing_enc
        }])

        cost = float(model.predict(input_df)[0])
        results[provider] = round(cost, 2)

    best_provider = min(results, key=results.get)
    worst_provider = max(results, key=results.get)

    return {
        "recommendation": best_provider,
        "predicted_costs": results,
        "savings_vs_most_expensive": round(results[worst_provider] - results[best_provider], 2)
    }