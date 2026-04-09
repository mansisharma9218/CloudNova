import pickle
import os
import pandas as pd

# ─── LOAD ARTIFACTS ───────────────────────────────────────────────────────────
model_dir = os.path.dirname(__file__)

with open(os.path.join(model_dir, "cost_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(model_dir, "encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)

pricing_table = pd.read_csv(os.path.join(model_dir, "pricing_table.csv"))

le_provider = encoders["provider"]
le_region   = encoders["region"]
le_pricing  = encoders["pricing"]

# All known combinations — used to enumerate recommendations
ALL_PROVIDERS     = list(le_provider.classes_)
ALL_REGIONS       = list(le_region.classes_)
ALL_PRICING_MODELS = list(le_pricing.classes_)


def _predict_hourly_rate(vcpu, ram_gb, storage_gb, provider, region, pricing_model):
    """
    Predict price_per_hour for a given configuration.
    Uses exact pricing table lookup first; falls back to ML for unseen configs.
    """
    # Exact lookup: match on provider, region, pricing_model, vcpu, ram_gb
    match = pricing_table[
        (pricing_table["provider"]      == provider) &
        (pricing_table["region"]        == region) &
        (pricing_table["pricing_model"] == pricing_model) &
        (pricing_table["vcpu"]          == vcpu) &
        (pricing_table["ram_gb"]        == ram_gb)
    ]

    if not match.empty:
        return float(match["price_per_hour"].iloc[0]), "exact"

    # ML fallback for unseen configurations
    input_df = pd.DataFrame([{
        "vcpu":              vcpu,
        "ram_gb":            ram_gb,
        "storage_gb":        storage_gb,
        "provider_enc":      le_provider.transform([provider])[0],
        "region_enc":        le_region.transform([region])[0],
        "pricing_model_enc": le_pricing.transform([pricing_model])[0],
    }])
    predicted_rate = model.predict(input_df)[0]
    return float(predicted_rate), "ml"


def predict_cost(vcpu, ram_gb, storage_gb, usage_hours, provider, region, pricing_model):
    """
    Predict monthly cost for a single specific configuration.
    Returns dict with cost, hourly rate, and source (exact/ml).
    """
    hourly_rate, source = _predict_hourly_rate(
        vcpu, ram_gb, storage_gb, provider, region, pricing_model
    )
    monthly_cost = hourly_rate * usage_hours

    return {
        "provider":      provider,
        "region":        region,
        "pricing_model": pricing_model,
        "price_per_hour": round(hourly_rate, 4),
        "monthly_cost":  round(monthly_cost, 2),
        "source":        source,  # "exact" or "ml"
    }


def recommend(vcpu, ram_gb, storage_gb, usage_hours,
              preferred_provider=None, preferred_region=None,
              top_n=5):
    """
    Given a workload spec, enumerate all provider/region/pricing_model
    combinations and return the top_n cheapest options.

    Args:
        vcpu, ram_gb, storage_gb, usage_hours: workload requirements
        preferred_provider: optionally filter to one provider (e.g. "AWS")
        preferred_region:   optionally filter to one region (e.g. "us-east")
        top_n: number of recommendations to return

    Returns:
        List of dicts sorted by monthly_cost ascending.
    """
    providers = [preferred_provider] if preferred_provider else ALL_PROVIDERS
    regions   = [preferred_region]   if preferred_region   else ALL_REGIONS

    results = []
    for provider in providers:
        for region in regions:
            for pricing_model in ALL_PRICING_MODELS:
                try:
                    result = predict_cost(
                        vcpu, ram_gb, storage_gb, usage_hours,
                        provider, region, pricing_model
                    )
                    results.append(result)
                except Exception:
                    # Skip if provider/region/pricing_model not in encoder
                    continue

    # Sort by monthly cost, cheapest first
    results.sort(key=lambda x: x["monthly_cost"])
    return results[:top_n]


# ─── EXAMPLE USAGE ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Single prediction ===")
    result = predict_cost(
        vcpu=2, ram_gb=4, storage_gb=50, usage_hours=720,
        provider="AWS", region="us-east", pricing_model="on-demand"
    )
    print(result)

    print("\n=== Top 5 cheapest options for this workload ===")
    recs = recommend(vcpu=2, ram_gb=4, storage_gb=50, usage_hours=720, top_n=5)
    print(f"{'Provider':<8} {'Region':<10} {'Model':<14} {'$/hr':>8} {'Monthly':>10} {'Source'}")
    print("-" * 65)
    for r in recs:
        print(f"{r['provider']:<8} {r['region']:<10} {r['pricing_model']:<14} "
              f"${r['price_per_hour']:>6.4f} ${r['monthly_cost']:>9.2f} {r['source']}")

    print("\n=== AWS-only recommendations ===")
    recs = recommend(vcpu=4, ram_gb=16, storage_gb=100, usage_hours=720,
                     preferred_provider="AWS", top_n=5)
    for r in recs:
        print(f"{r['provider']:<8} {r['region']:<10} {r['pricing_model']:<14} "
              f"${r['price_per_hour']:>6.4f} ${r['monthly_cost']:>9.2f}")