"""
train.py — CloudNova ML Model Training
Target: price_per_hour  (monthly_cost = price_per_hour × usage_hours)

"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
print("Loading data...")
BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "data.csv"))

df = df[(df["monthly_cost"] >= 5) & (df["monthly_cost"] <= 2000)].copy()
print(f"Total records after filter: {len(df)}")

# ── ENCODE CATEGORICALS ────────────────────────────────────────────────────────
le_provider = LabelEncoder()
le_region   = LabelEncoder()
le_pricing  = LabelEncoder()

df["provider_enc"]      = le_provider.fit_transform(df["provider"])
df["region_enc"]        = le_region.fit_transform(df["region"])
df["pricing_model_enc"] = le_pricing.fit_transform(df["pricing_model"])

# ── FEATURE ENGINEERING ────────────────────────────────────────────────────────

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

# ── TRAIN / TEST SPLIT ─────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train: {len(X_train)}  |  Test: {len(X_test)}")

# ── TRAIN ──────────────────────────────────────────────────────────────────────
print("Training Random Forest (target = price_per_hour)...")
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=3,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# ── EVALUATE ───────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2   = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"  MAE  : ${mae:.4f}/hr")
print(f"  RMSE : ${rmse:.4f}/hr")
print(f"  R²   : {r2:.4f}")

# ── FEATURE IMPORTANCE ─────────────────────────────────────────────────────────
fi = pd.DataFrame({
    "feature":    FEATURES,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)
print(f"\nFeature Importance:\n{fi.to_string(index=False)}")

# ── SAVE ───────────────────────────────────────────────────────────────────────
with open(os.path.join(BASE_DIR, "cost_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(BASE_DIR, "encoders.pkl"), "wb") as f:
    pickle.dump({
        "provider": le_provider,
        "region":   le_region,
        "pricing":  le_pricing,
    }, f)

# Save pred-vs-actual sample for Insights page
sample = pd.DataFrame({"actual": y_test.values, "predicted": y_pred})
sample = sample.sample(150, random_state=42).round(4)
sample.to_csv(os.path.join(BASE_DIR, "pred_vs_actual.csv"), index=False)

# Save feature importance for Insights page
FEATURE_LABELS = {
    "vcpu":              "vCPU",
    "ram_gb":            "RAM (GB)",
    "storage_gb":        "Storage (GB)",
    "provider_enc":      "Provider",
    "region_enc":        "Region",
    "pricing_model_enc": "Pricing Model",
}
fi["label"] = fi["feature"].map(FEATURE_LABELS)
fi["importance"] = (fi["importance"] * 100).round(2)
fi[["label", "importance"]].to_csv(
    os.path.join(BASE_DIR, "feature_importance.csv"), index=False
)

print("\nSaved: cost_model.pkl, encoders.pkl, pred_vs_actual.csv, feature_importance.csv")

# ── SANITY CHECK ───────────────────────────────────────────────────────────────
print("\nSanity check (spot < on-demand < europe?):")
def _predict(vcpu, ram, stor, prov, reg, pm):
    row = pd.DataFrame([{
        "vcpu": vcpu, "ram_gb": ram, "storage_gb": stor,
        "provider_enc":      le_provider.transform([prov])[0],
        "region_enc":        le_region.transform([reg])[0],
        "pricing_model_enc": le_pricing.transform([pm])[0],
    }])
    return model.predict(row)[0]

spot = _predict(2, 4, 50, "AWS", "us-east", "spot")
od   = _predict(2, 4, 50, "AWS", "us-east", "on-demand")
eu   = _predict(2, 4, 50, "AWS", "europe",  "on-demand")
print(f"  spot={spot:.4f}  on-demand={od:.4f}  europe-on-demand={eu:.4f}")
print(f"  spot < on-demand: {spot < od}")
print(f"  europe > us-east: {eu > od}")
