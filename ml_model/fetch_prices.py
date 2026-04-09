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

# 🌍 REGION EFFECT
REGION_MULT = {
    "us-east": 1.00,
    "us-west": 1.06,
    "europe":  1.10,
    "asia":    1.15,
}

# ☁️ PROVIDER NOISE (NO BIAS, REALISTIC)
PROVIDER_NOISE = {
    "AWS":   (0.98, 1.04),
    "Azure": (1.00, 1.06),
    "GCP":   (0.96, 1.02),
}

# 💰 PRICING TIERS (STRICT ORDER)
PRICING_MULT = {
    "spot":         (0.50, 0.60),
    "3yr-reserved": (0.65, 0.75),
    "1yr-reserved": (0.80, 0.90),
    "on-demand":    (0.95, 1.05),
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

    # ✅ realistic constraint
    if ram < vcpu or ram > vcpu * 16:
        continue

    # 🧠 NON-LINEAR BASE PRICE (CALIBRATED)
    base_price = (
        (vcpu ** 1.05) * 0.030 +
        (ram ** 1.02) * 0.0042 +
        (storage * 0.00012)
    ) + 0.01

    # 🌍 region impact
    base_price *= REGION_MULT[region]

    # ☁️ provider small variation (NO bias)
    low_p, high_p = PROVIDER_NOISE[provider]
    base_price *= random.uniform(low_p, high_p)

    # 💰 pricing model impact
    low, high = PRICING_MULT[pricing]
    price = base_price * random.uniform(low, high)

    # 📊 outputs
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