from __future__ import annotations

from fastapi import APIRouter, Depends

from auth import verify_token
from utils.cost_utils import compute_cost
from routes.predict import (
    model, le_provider, le_region, le_pricing,
    _best_instance, PROVIDERS,
)

router = APIRouter()


@router.post("/")
def get_recommendation(
    vcpu: int,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    region: str = "us-east",
    pricing_model: str = "on-demand",
    budget: float = None,
    user=Depends(verify_token),
):

    instance_picks = {
        p: _best_instance(
            p, vcpu, ram_gb, storage_gb, usage_hours, region, pricing_model
        )
        for p in PROVIDERS
    }

    costs = {
        p: instance_picks[p]["monthly_cost"]
        for p in PROVIDERS
    }

    best = min(costs, key=costs.get)
    worst = max(costs, key=costs.get)
    savings = round(costs[worst] - costs[best], 2)

    return {
        "best_provider": best,
        "costs": costs,
        "instance_picks": instance_picks,
        "savings": savings,
    }
