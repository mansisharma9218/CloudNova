from fastapi import APIRouter
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

months = ["Jan","Feb","Mar","Apr","May","Jun"]

@router.get("/")
def get_trends():

    results = []

    for i, month in enumerate(months):

        hours = 360 + i * 60

        providers = {}

        for provider in ["AWS","Azure","GCP"]:

            df = pd.DataFrame([{
                "vcpu": 4,
                "ram_gb": 8,
                "storage_gb": 50,
                "usage_hours": hours,
                "price_per_vcpu": 0.05,
                "provider_enc": encoders["provider"].transform([provider])[0],
                "region_enc": encoders["region"].transform(["us-east"])[0],
                "pricing_model_enc": encoders["pricing"].transform(["on-demand"])[0],
            }])

            cost = float(model.predict(df)[0])
            providers[provider] = round(cost,2)

        results.append({
            "month": month,
            **providers
        })

    return results