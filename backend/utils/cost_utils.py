import pandas as pd

def compute_cost(
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
):
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
    return round(cost, 2)