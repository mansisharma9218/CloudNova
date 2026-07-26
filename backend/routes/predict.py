from __future__ import annotations

import os
import pickle

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends

from auth import verify_token
from routes.utils.cost_utils import compute_cost, predict_hourly_cost

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ML_DIR   = os.path.join(BASE_DIR, "..", "ml_model")

with open(os.path.join(ML_DIR, "cost_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(ML_DIR, "encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)

le_provider = encoders["provider"]
le_region   = encoders["region"]
le_pricing  = encoders["pricing"]

# Instance catalog: provider, instance_type, vcpu, ram_gb, storage_gb
CATALOG = pd.read_csv(os.path.join(ML_DIR, "instance_catalog.csv"))

PROVIDERS  = ["AWS", "Azure", "GCP"]
TOP_K      = 5   # candidates per provider before ML ranking


def _best_instance(
    provider: str,
    req_vcpu: float,
    req_ram: float,
    req_storage: float,
    usage_hours: float,
    region: str,
    pricing_model: str,
) -> dict:
    """
    Given a provider and workload spec, return the cheapest ML-ranked instance.
    Filter by vcpu + ram only (storage is always independently attachable in all clouds).
    """
    prov_df = CATALOG[CATALOG["provider"] == provider].copy()


    valid = prov_df[
        (prov_df["vcpu"]   >= req_vcpu) &
        (prov_df["ram_gb"] >= req_ram)
    ].copy()


    used_fallback = False

    if valid.empty:
        used_fallback = True

        prov_df["_score"] = (
            np.maximum(0.0, req_vcpu  - prov_df["vcpu"]) * 1000 +  
            np.maximum(0.0, req_ram   - prov_df["ram_gb"]) * 1000 +
            prov_df["vcpu"] * 1 +                                 
            prov_df["ram_gb"] * 0.5
        )

        valid = prov_df.nsmallest(TOP_K, "_score").copy()

    else:

        valid = valid.sort_values(["vcpu", "ram_gb"]).head(TOP_K)

      
        best_hourly = float("inf")

        for _, row in valid.iterrows():
            hourly = predict_hourly_cost(
                model, le_provider, le_region, le_pricing,
                vcpu=row["vcpu"],
                ram_gb=row["ram_gb"],
                storage_gb=req_storage,      
                provider=provider,
                region=region,
                pricing_model=pricing_model,
            )
            if hourly < best_hourly:
                best_hourly = hourly
                best_row    = row

        return {
            "instance_type":        str(best_row["instance_type"]),
            "vcpu":                 int(best_row["vcpu"]),
            "ram_gb":               float(best_row["ram_gb"]),
            "storage_gb":           float(req_storage),
            "predicted_hourly_cost": round(best_hourly, 4),
            "monthly_cost":         round(best_hourly * usage_hours, 2),
            "fallback":             used_fallback,
        }


@router.post("/")
def predict_cost(
    vcpu: int,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    region: str,
    pricing_model: str,
    user=Depends(verify_token),
):
    instance_picks = {}
    results = {}

    for provider in PROVIDERS:
        best = _best_instance(
            provider=provider,
            req_vcpu=vcpu,
            req_ram=ram_gb,
            req_storage=storage_gb,
            usage_hours=usage_hours,
            region=region,
            pricing_model=pricing_model,
        )

        instance_picks[provider] = best
        results[provider] = best["monthly_cost"]

    best_provider = min(results, key=results.get)
    worst_provider = max(results, key=results.get)

    return {
        "recommendation": best_provider,
        "predicted_costs": results,
        "instance_picks": instance_picks,
        "savings_vs_most_expensive": round(results[worst_provider] - results[best_provider], 2),
    }


@router.post("/instance")
def recommend_instance(
    vcpu: int,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    region: str          = "us-east",
    pricing_model: str   = "on-demand",
    user=Depends(verify_token),
):
    recommendations: dict[str, dict] = {}
    for provider in PROVIDERS:
        recommendations[provider] = _best_instance(
            provider=provider,
            req_vcpu=vcpu,
            req_ram=ram_gb,
            req_storage=storage_gb,
            usage_hours=usage_hours,
            region=region,
            pricing_model=pricing_model,
        )

    best_provider = min(
        recommendations,
        key=lambda p: recommendations[p]["monthly_cost"],
    )

    return {
        "best_provider":   best_provider,
        "recommendations": recommendations,
    }