import pandas as pd
import itertools
import random

providers = ["AWS", "Azure", "GCP"]
regions = ["us-east", "us-west", "europe", "asia"]
pricing_models = ["on-demand", "spot", "1yr-reserved", "3yr-reserved"]
usage_hours_list = [180, 360, 540, 720]

vcpu_options = [1, 2, 4, 8, 16, 32, 64]
ram_options = [2, 4, 8, 16, 32, 64, 128, 256, 512]
storage_options = [20, 50, 100, 200, 400, 800, 1000, 2000]

rows = []

for vcpu, ram, storage in itertools.product(vcpu_options, ram_options, storage_options):

    # avoid unrealistic combos
    if ram < vcpu:
        continue

    base_price = (
        0.02 * vcpu +
        0.005 * ram +
        0.0005 * storage
    )

    for provider in providers:
        for region in regions:
            for pricing in pricing_models:
                for usage in usage_hours_list:

                    price = base_price

                    # provider modifier
                    if provider == "Azure":
                        price *= 1.05
                    elif provider == "GCP":
                        price *= 1.03

                    # region modifier
                    if region == "europe":
                        price *= 1.15
                    elif region == "asia":
                        price *= 1.20

                    # pricing model modifier
                    if pricing == "spot":
                        price *= 0.6
                    elif pricing == "1yr-reserved":
                        price *= 0.8
                    elif pricing == "3yr-reserved":
                        price *= 0.7

                    # small randomness (VERY IMPORTANT for ML)
                    price *= random.uniform(0.95, 1.05)

                    monthly_cost = price * usage

                    rows.append({
                        "provider": provider,
                        "vcpu": vcpu,
                        "ram_gb": ram,
                        "storage_gb": storage,
                        "usage_hours": usage,
                        "region": region,
                        "pricing_model": pricing,
                        "price_per_hour": round(price, 4),
                        "monthly_cost": round(monthly_cost, 2),
                    })

df = pd.DataFrame(rows)

# limit size (optional)
df = df.sample(4000, random_state=42)

df.to_csv("data.csv", index=False)

print("data.csv generated with", len(df), "rows")