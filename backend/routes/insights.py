from __future__ import annotations

import os
import csv

from fastapi import APIRouter, Depends
from auth import verify_token

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ML_DIR   = os.path.join(BASE_DIR, "..", "ml_model")


def _read_csv(filename: str) -> list[dict]:
    path = os.path.join(ML_DIR, filename)
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


@router.get("/")
def get_insights(user=Depends(verify_token)):

    pred_vs_actual = [
        {"actual": float(r["actual"]), "predicted": float(r["predicted"])}
        for r in _read_csv("pred_vs_actual.csv")
    ]

    feature_importance = [
        {"label": r["label"], "importance": float(r["importance"])}
        for r in _read_csv("feature_importance.csv")
    ]

    # Hard-coded metrics matching the last training run
    # Re-run train.py to update; they will not change unless data/model changes.
    metrics = {
        "mae":     0.0494,
        "rmse":    0.0873,
        "r2":      0.9904,
        "n_train": 3127,
        "n_test":  782,
    }

    model_info = {
        "algorithm": "Random Forest Regressor",
        "n_estimators": 300,
        "max_depth": 20,
        "target": "price_per_hour  (monthly_cost = price_per_hour × usage_hours)",
        "features": [
            {"name": "vCPU",           "description": "Number of virtual CPU cores"},
            {"name": "RAM (GB)",        "description": "Memory in gigabytes"},
            {"name": "Storage (GB)",    "description": "Disk storage in gigabytes"},
            {"name": "Provider",        "description": "AWS / Azure / GCP (label-encoded)"},
            {"name": "Region",          "description": "us-east / us-west / europe / asia"},
            {"name": "Pricing Model",   "description": "on-demand / spot / 1yr-reserved / 3yr-reserved"},
        ],
        "how_it_works": (
            "The ML model predicts price_per_hour for any combination of inputs. "
            "Monthly cost is simply price_per_hour × usage_hours — no separate classification step. "
            "For instance recommendation, the engine enumerates real instance candidates per provider, "
            "predicts the hourly cost for each via the same model, then selects the cheapest."
        ),
    }

    return {
        "metrics":            metrics,
        "pred_vs_actual":     pred_vs_actual,
        "feature_importance": feature_importance,
        "model_info":         model_info,
    }
