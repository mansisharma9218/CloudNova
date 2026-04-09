import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# LOAD DATA 
print("Loading data...")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data.csv"))

# Filter to realistic range
df = df[(df["monthly_cost"] >= 5) & (df["monthly_cost"] <= 2000)].copy()

print(f"Total records: {len(df)}")
print(df.groupby(["provider", "pricing_model"])["price_per_hour"].count())
print(f"\nprice_per_hour range: ${df['price_per_hour'].min():.4f} - ${df['price_per_hour'].max():.4f}")

# ENCODE CATEGORICAL FEATURES 
le_provider = LabelEncoder()
le_region   = LabelEncoder()
le_pricing  = LabelEncoder()

df["provider_enc"]      = le_provider.fit_transform(df["provider"])
df["region_enc"]        = le_region.fit_transform(df["region"])
df["pricing_model_enc"] = le_pricing.fit_transform(df["pricing_model"])

print("\nProvider encoding:", dict(zip(le_provider.classes_, le_provider.transform(le_provider.classes_))))
print("Region encoding:",   dict(zip(le_region.classes_,   le_region.transform(le_region.classes_))))
print("Pricing encoding:",  dict(zip(le_pricing.classes_,  le_pricing.transform(le_pricing.classes_))))

# FEATURES AND TARGET 
FEATURES = [
    "vcpu",
    "ram_gb",
    "storage_gb",
    "provider_enc",
    "region_enc",
    "pricing_model_enc",
]

X = df[FEATURES]
y = df["price_per_hour"]

# TRAIN TEST SPLIT 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# TRAIN MODEL 
print("\nTraining Random Forest model (target = price_per_hour)...")
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=3,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# EVALUATE 
y_pred = model.predict(X_test)
mae  = mean_absolute_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)

print(f"\nModel Performance (predicting price_per_hour):")
print(f"  MAE: ${mae:.4f}/hr  (average hourly rate prediction error)")
print(f"  R2:  {r2:.4f}   (1.0 = perfect, >0.90 = good, >0.95 = excellent)")

# FEATURE IMPORTANCE 
importance = pd.DataFrame({
    "feature":    FEATURES,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)
print(f"\nFeature Importance:")
print(importance.to_string(index=False))

# SAVE MODEL AND ENCODERS 
model_dir = os.path.dirname(__file__)

with open(os.path.join(model_dir, "cost_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(model_dir, "encoders.pkl"), "wb") as f:
    pickle.dump({
        "provider": le_provider,
        "region":   le_region,
        "pricing":  le_pricing,
    }, f)

print("\nModel saved to ml_model/cost_model.pkl")
print("Encoders saved to ml_model/encoders.pkl")
print("Pricing table preserved at ml_model/pricing_table.csv (managed by fix_pricing_table.py)")

# SANITY CHECK 
# We predict price_per_hour, then multiply by usage_hours to get monthly cost.
# Spot should predict lower than on-demand. Europe should predict higher than us-east.
print("\nSanity check — predicted monthly costs (720 hrs):")
test_cases = [
    {"vcpu": 2, "ram_gb": 4,  "storage_gb": 50,  "provider": "AWS",   "region": "us-east", "pricing_model": "on-demand",    "expected_monthly": "~$69"},
    {"vcpu": 2, "ram_gb": 4,  "storage_gb": 50,  "provider": "AWS",   "region": "us-east", "pricing_model": "spot",         "expected_monthly": "~$46"},
    {"vcpu": 2, "ram_gb": 4,  "storage_gb": 50,  "provider": "AWS",   "region": "us-east", "pricing_model": "1yr-reserved", "expected_monthly": "~$58"},
    {"vcpu": 2, "ram_gb": 4,  "storage_gb": 50,  "provider": "GCP",   "region": "us-east", "pricing_model": "on-demand",    "expected_monthly": "~$68"},
    {"vcpu": 2, "ram_gb": 4,  "storage_gb": 50,  "provider": "AWS",   "region": "europe",  "pricing_model": "on-demand",    "expected_monthly": "~$79"},
    {"vcpu": 4, "ram_gb": 16, "storage_gb": 100, "provider": "AWS",   "region": "us-east", "pricing_model": "on-demand",    "expected_monthly": "~$145"},
]

usage_hours = 720
print(f"{'Provider':<8} {'Region':<10} {'Model':<14} {'$/hr':>8} {'Monthly':>10} {'Expected':<15}")
print("-" * 70)

for tc in test_cases:
    input_df = pd.DataFrame([{
        "vcpu":              tc["vcpu"],
        "ram_gb":            tc["ram_gb"],
        "storage_gb":        tc["storage_gb"],
        "provider_enc":      le_provider.transform([tc["provider"]])[0],
        "region_enc":        le_region.transform([tc["region"]])[0],
        "pricing_model_enc": le_pricing.transform([tc["pricing_model"]])[0],
    }])
    pred_hourly  = model.predict(input_df)[0]
    pred_monthly = pred_hourly * usage_hours
    print(f"{tc['provider']:<8} {tc['region']:<10} {tc['pricing_model']:<14} "
          f"${pred_hourly:>6.4f} ${pred_monthly:>9.2f} {tc['expected_monthly']:<15}")

print()
print("Key checks:")
print("  spot < on-demand for same config?", end=" ")
results = {}
for tc in test_cases[:3]:
    input_df = pd.DataFrame([{
        "vcpu": tc["vcpu"], "ram_gb": tc["ram_gb"], "storage_gb": tc["storage_gb"],
        "provider_enc":      le_provider.transform([tc["provider"]])[0],
        "region_enc":        le_region.transform([tc["region"]])[0],
        "pricing_model_enc": le_pricing.transform([tc["pricing_model"]])[0],
    }])
    results[tc["pricing_model"]] = model.predict(input_df)[0]

spot_ok     = results["spot"] < results["on-demand"]
reserved_ok = results["1yr-reserved"] < results["on-demand"]
print(" YES" if spot_ok else " NO — data issue")
print(f"  1yr-reserved < on-demand?          ", " YES" if reserved_ok else " NO — data issue")

eu_df = pd.DataFrame([{"vcpu": 2, "ram_gb": 4, "storage_gb": 50,
    "provider_enc":      le_provider.transform(["AWS"])[0],
    "region_enc":        le_region.transform(["europe"])[0],
    "pricing_model_enc": le_pricing.transform(["on-demand"])[0]}])
use_df = pd.DataFrame([{"vcpu": 2, "ram_gb": 4, "storage_gb": 50,
    "provider_enc":      le_provider.transform(["AWS"])[0],
    "region_enc":        le_region.transform(["us-east"])[0],
    "pricing_model_enc": le_pricing.transform(["on-demand"])[0]}])
europe_more = model.predict(eu_df)[0] > model.predict(use_df)[0]
print(f"  europe > us-east (same config)?    ", " YES" if europe_more else " NO — data issue")
