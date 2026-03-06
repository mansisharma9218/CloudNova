import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data.csv"))

# Filter to realistic user range
df = df[df["monthly_cost"] <= 2000]
df = df[df["monthly_cost"] >= 5]
df = df.copy()

# Add variation to usage_hours and storage_gb so they matter to the model
np.random.seed(42)
df["usage_hours"] = np.random.choice([180, 360, 540, 720], size=len(df))
df["storage_gb"]  = np.random.choice([20, 50, 100, 200, 500], size=len(df))

# Recalculate monthly_cost to reflect actual usage hours
df["monthly_cost"] = (df["price_per_hour"] * df["usage_hours"]).round(2)

# Filter again after recalculation
df = df[df["monthly_cost"] >= 1]
df = df[df["monthly_cost"] <= 2000]

print(f"Total records: {len(df)}")
print(df.groupby(["provider", "pricing_model"])["monthly_cost"].count())
print(f"\nCost range: ${df['monthly_cost'].min():.2f} - ${df['monthly_cost'].max():.2f}")

# ─── ENCODE CATEGORICAL FEATURES ──────────────────────────────────────────────
le_provider = LabelEncoder()
le_region   = LabelEncoder()
le_pricing  = LabelEncoder()

df["provider_enc"]      = le_provider.fit_transform(df["provider"])
df["region_enc"]        = le_region.fit_transform(df["region"])
df["pricing_model_enc"] = le_pricing.fit_transform(df["pricing_model"])

print("\nProvider encoding:", dict(zip(le_provider.classes_, le_provider.transform(le_provider.classes_))))
print("Region encoding:",   dict(zip(le_region.classes_,   le_region.transform(le_region.classes_))))
print("Pricing encoding:",  dict(zip(le_pricing.classes_,  le_pricing.transform(le_pricing.classes_))))

# ─── FEATURES AND TARGET ──────────────────────────────────────────────────────
FEATURES = [
    "vcpu",
    "ram_gb",
    "storage_gb",
    "usage_hours",
    "price_per_vcpu",
    "provider_enc",
    "region_enc",
    "pricing_model_enc",
]

X = df[FEATURES]
y = df["monthly_cost"]

# ─── TRAIN TEST SPLIT ─────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# ─── TRAIN MODEL ──────────────────────────────────────────────────────────────
print("\nTraining Random Forest model...")
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=3,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# ─── EVALUATE ─────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"  MAE: ${mae:.2f}  (average prediction error in dollars)")
print(f"  R2:  {r2:.4f}   (1.0 = perfect, >0.90 = good, >0.95 = excellent)")

# ─── FEATURE IMPORTANCE ───────────────────────────────────────────────────────
importance = pd.DataFrame({
    "feature":    FEATURES,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)
print(f"\nFeature Importance:")
print(importance.to_string(index=False))

# ─── SAVE MODEL AND ENCODERS ──────────────────────────────────────────────────
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

# ─── SANITY CHECK ─────────────────────────────────────────────────────────────
print("\nSanity check predictions:")
test_cases = [
    # Small instance full month
    {"vcpu": 2,  "ram_gb": 4,   "storage_gb": 50,  "usage_hours": 720, "provider": "AWS",   "region": "us-east", "pricing_model": "on-demand",    "expected": "~$30-50"},
    {"vcpu": 2,  "ram_gb": 4,   "storage_gb": 50,  "usage_hours": 720, "provider": "Azure", "region": "us-east", "pricing_model": "on-demand",    "expected": "~$30-50"},
    {"vcpu": 2,  "ram_gb": 4,   "storage_gb": 50,  "usage_hours": 720, "provider": "GCP",   "region": "us-east", "pricing_model": "on-demand",    "expected": "~$24-30"},
    # Reserved saves money
    {"vcpu": 4,  "ram_gb": 16,  "storage_gb": 100, "usage_hours": 720, "provider": "AWS",   "region": "us-east", "pricing_model": "1yr-reserved", "expected": "~$50-80"},
    # Spot is cheapest
    {"vcpu": 4,  "ram_gb": 16,  "storage_gb": 100, "usage_hours": 720, "provider": "AWS",   "region": "us-east", "pricing_model": "spot",         "expected": "~$20-30"},
    # Europe costs more
    {"vcpu": 2,  "ram_gb": 8,   "storage_gb": 50,  "usage_hours": 720, "provider": "AWS",   "region": "europe",  "pricing_model": "on-demand",    "expected": "~$60-80"},
    # Half month usage
    {"vcpu": 2,  "ram_gb": 4,   "storage_gb": 50,  "usage_hours": 360, "provider": "GCP",   "region": "us-east", "pricing_model": "on-demand",    "expected": "~$12-15"},
    # Large instance
    {"vcpu": 16, "ram_gb": 64,  "storage_gb": 200, "usage_hours": 720, "provider": "AWS",   "region": "us-east", "pricing_model": "on-demand",    "expected": "~$500-800"},
]

print(f"{'Provider':<8} {'Region':<10} {'Model':<14} {'Specs':<20} {'Predicted':>12} {'Expected':<15}")
print("-" * 85)

for tc in test_cases:

    # estimate price_per_vcpu similar to training logic
    base_price = (tc["vcpu"] * 0.045) + (tc["ram_gb"] * 0.006)
    monthly_estimate = base_price * tc["usage_hours"]
    price_per_vcpu = monthly_estimate / tc["vcpu"]

    input_df = pd.DataFrame([{
        "vcpu":              tc["vcpu"],
        "ram_gb":            tc["ram_gb"],
        "storage_gb":        tc["storage_gb"],
        "usage_hours":       tc["usage_hours"],
        "price_per_vcpu":    price_per_vcpu,
        "provider_enc":      le_provider.transform([tc["provider"]])[0],
        "region_enc":        le_region.transform([tc["region"]])[0],
        "pricing_model_enc": le_pricing.transform([tc["pricing_model"]])[0],
    }])

    pred  = model.predict(input_df)[0]
    specs = f"{tc['vcpu']}vCPU {tc['ram_gb']}GB {tc['usage_hours']}hrs"

    print(f"{tc['provider']:<8} {tc['region']:<10} {tc['pricing_model']:<14} {specs:<20} ${pred:>10.2f} {tc['expected']:<15}")