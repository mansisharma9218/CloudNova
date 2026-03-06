import pandas as pd
import itertools
import random

random.seed(42)

print("Generating expanded dataset...")

vcpu_values    = [1, 2, 4, 8, 16, 32]
ram_values     = [2, 4, 8, 16, 32, 64, 128]
storage_values = [20, 50, 100, 200, 500]
usage_hours    = [180, 360, 540, 720]
regions        = ["us-east", "us-west", "europe", "asia"]
pricing_models = ["on-demand", "spot", "1yr-reserved", "3yr-reserved"]
providers      = ["AWS", "Azure", "GCP"]

REGION_MULT = {
    "us-east": 1.00,
    "us-west": 1.08,
    "europe":  1.12,
    "asia":    1.20,
}

PROVIDER_MULT = {
    "AWS":   1.00,
    "Azure": 0.99,
    "GCP":   0.97,
}

PRICING_MULT = {
    "on-demand":    (0.95, 1.05),
    "spot":         (0.55, 0.75),
    "1yr-reserved": (0.75, 0.90),
    "3yr-reserved": (0.65, 0.85),
}

records = []

for provider, vcpu, ram, storage, hours, region, pricing in itertools.product(
    providers,
    vcpu_values,
    ram_values,
    storage_values,
    usage_hours,
    regions,
    pricing_models
):
    # realistic RAM/CPU constraint
    if ram < vcpu or ram > vcpu * 16:
        continue

    # 1. base compute cost
    base_price = (vcpu * 0.04) + (ram * 0.005) + (storage * 0.0005)

    # 2. provider adjustment
    base_price *= PROVIDER_MULT[provider]

    # 3. region adjustment
    base_price *= REGION_MULT[region]

    # 4. pricing model adjustment
    low, high = PRICING_MULT[pricing]
    price = base_price * random.uniform(low, high)

    if provider == "Azure" and pricing in ["1yr-reserved", "3yr-reserved"]:
        price *= 0.78

    if provider == "GCP" and pricing == "spot":
        price *= 0.80

    if provider == "AWS" and pricing == "on-demand":
        price *= 0.92

    # 5. monthly cost
    monthly_cost = price * hours

    price_per_vcpu = price / vcpu

    records.append({
        "provider":      provider,
        "vcpu":          vcpu,
        "ram_gb":        ram,
        "storage_gb":    storage,
        "usage_hours":   hours,
        "region":        region,
        "pricing_model": pricing,
        "price_per_hour": round(price, 4),
        "monthly_cost":   round(monthly_cost, 2),
        "price_per_vcpu": round(price_per_vcpu, 2)
    })

df = pd.DataFrame(records)
print(f"Dataset size: {len(df)}")
print(df.groupby(["provider", "pricing_model"])["monthly_cost"].mean().round(2))
df.to_csv("ml_model/data.csv", index=False)
print("Saved to ml_model/data.csv")