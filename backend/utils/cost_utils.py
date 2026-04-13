from __future__ import annotations
import functools
import pandas as pd

def _build_input(
    vcpu,
    ram_gb,
    storage_gb,
    provider_enc,
    region_enc,
    pricing_enc,
):
    return pd.DataFrame([{
        "vcpu": float(vcpu),
        "ram_gb": float(ram_gb),
        "storage_gb": float(storage_gb),
        "provider_enc": provider_enc,
        "region_enc": region_enc,
        "pricing_model_enc": pricing_enc,
    }])

@functools.lru_cache(maxsize=512)
def _cached_predict(
    model_id: int,          # id(model) — invalidates cache if model changes
    vcpu: float,
    ram_gb: float,
    storage_gb: float,
    provider_enc: int,
    region_enc: int,
    pricing_enc: int,
) -> float:
    from routes.predict import model   # noqa: PLC0415
    df = _build_input(vcpu, ram_gb, storage_gb, provider_enc, region_enc, pricing_enc)
    return float(model.predict(df)[0])

def predict_hourly_cost(
    model,
    le_provider,
    le_region,
    le_pricing,
    vcpu: float,
    ram_gb: float,
    storage_gb: float,
    provider: str,
    region: str,
    pricing_model: str,
) -> float:
    p_enc = int(le_provider.transform([provider])[0])
    r_enc = int(le_region.transform([region])[0])
    pm_enc = int(le_pricing.transform([pricing_model])[0])

    return _cached_predict(
        id(model),
        float(vcpu), float(ram_gb), float(storage_gb),
        p_enc, r_enc, pm_enc,
    )


def compute_cost(
    model,
    le_provider,
    le_region,
    le_pricing,
    vcpu: float,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    provider: str,
    region: str,
    pricing_model: str,
) -> float:
    hourly = predict_hourly_cost(
        model, le_provider, le_region, le_pricing,
        vcpu, ram_gb, storage_gb, provider, region, pricing_model,
    )
    return round(hourly * usage_hours, 2)
