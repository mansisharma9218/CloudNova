from fastapi import APIRouter, Depends
from auth import verify_token
import pickle
import pandas as pd
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "cost_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "ml_model", "encoders.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(ENCODER_PATH, "rb") as f:
    encoders = pickle.load(f)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

@router.get("/")
def get_trends(user=Depends(verify_token)):

    results = []

    # realistic workload pattern
    usage_hours = [320, 400, 400, 650, 500, 600]

    # pricing strategy evolution
    pricing_models = [
        "on-demand",      # Jan
        "on-demand",      # Feb
        "1yr-reserved",   # Mar (optimization)
        "on-demand",      # Apr (spike)
        "spot",           # May (cost saving)
        "on-demand"       # Jun (scale up again)
    ]

    # mostly stable region (realistic)
    region = "us-east"

    # slight provider differences (real-world pricing gaps)
    provider_factor = {
        "AWS": 1.0,
        "Azure": 1.05,
        "GCP": 0.95
    }

    for i, month in enumerate(months):

        providers = {}

        for provider in ["AWS", "Azure", "GCP"]:

            df = pd.DataFrame([{
                "vcpu": 4,
                "ram_gb": 8,
                "storage_gb": 50,
                "provider_enc": encoders["provider"].transform([provider])[0],
                "region_enc": encoders["region"].transform([region])[0],
                "pricing_model_enc": encoders["pricing"].transform([pricing_models[i]])[0],
            }])

            price_per_hour = float(model.predict(df)[0])

            total_cost = price_per_hour * usage_hours[i]

            # apply provider variation
            total_cost *= provider_factor[provider]

            providers[provider] = round(total_cost, 2)

        results.append({
            "month": month,
            **providers
        })

    return results