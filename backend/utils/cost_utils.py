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

    # Match EXACTLY the 6 features the model was trained on
    input_df = pd.DataFrame([{
        "vcpu": vcpu,
        "ram_gb": ram_gb,
        "storage_gb": storage_gb,
        "provider_enc": provider_enc,
        "region_enc": region_enc,
        "pricing_model_enc": pricing_enc
    }])

    # Model predicts price_per_hour — multiply by hours to get total cost
    price_per_hour = float(model.predict(input_df)[0])
    total_cost = price_per_hour * usage_hours
    return round(total_cost, 2)