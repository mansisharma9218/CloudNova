from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data to avoid duplicates on re-seed
db.query(models.CloudPricing).delete()
db.commit()

pricing_data = [

    # ─────────────────────────────────────────────
    # AWS — us-east-1
    # ─────────────────────────────────────────────
    # on-demand
    models.CloudPricing(provider="AWS", instance_type="t3.micro",    vcpu=2,  ram_gb=1,   storage_gb=20,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0104,  monthly_cost=7.49),
    models.CloudPricing(provider="AWS", instance_type="t3.small",    vcpu=2,  ram_gb=2,   storage_gb=20,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0208,  monthly_cost=14.98),
    models.CloudPricing(provider="AWS", instance_type="t3.medium",   vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0416,  monthly_cost=29.95),
    models.CloudPricing(provider="AWS", instance_type="t3.large",    vcpu=2,  ram_gb=8,   storage_gb=50,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0832,  monthly_cost=59.90),
    models.CloudPricing(provider="AWS", instance_type="m5.large",    vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0960,  monthly_cost=69.12),
    models.CloudPricing(provider="AWS", instance_type="m5.xlarge",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1920,  monthly_cost=138.24),
    models.CloudPricing(provider="AWS", instance_type="m5.2xlarge",  vcpu=8,  ram_gb=32,  storage_gb=200, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.3840,  monthly_cost=276.48),
    models.CloudPricing(provider="AWS", instance_type="m5.4xlarge",  vcpu=16, ram_gb=64,  storage_gb=500, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.7680,  monthly_cost=552.96),
    models.CloudPricing(provider="AWS", instance_type="c5.large",    vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0850,  monthly_cost=61.20),
    models.CloudPricing(provider="AWS", instance_type="c5.xlarge",   vcpu=4,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1700,  monthly_cost=122.40),
    models.CloudPricing(provider="AWS", instance_type="r5.large",    vcpu=2,  ram_gb=16,  storage_gb=100, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1260,  monthly_cost=90.72),
    models.CloudPricing(provider="AWS", instance_type="r5.xlarge",   vcpu=4,  ram_gb=32,  storage_gb=200, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.2520,  monthly_cost=181.44),

    # spot
    models.CloudPricing(provider="AWS", instance_type="t3.medium",   vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0125,  monthly_cost=9.00),
    models.CloudPricing(provider="AWS", instance_type="m5.large",    vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0288,  monthly_cost=20.74),
    models.CloudPricing(provider="AWS", instance_type="m5.xlarge",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0576,  monthly_cost=41.47),
    models.CloudPricing(provider="AWS", instance_type="c5.xlarge",   vcpu=4,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0510,  monthly_cost=36.72),

    # 1yr-reserved
    models.CloudPricing(provider="AWS", instance_type="t3.medium",   vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.0263,  monthly_cost=18.94),
    models.CloudPricing(provider="AWS", instance_type="m5.large",    vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.0590,  monthly_cost=42.48),
    models.CloudPricing(provider="AWS", instance_type="m5.xlarge",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.1180,  monthly_cost=84.96),
    models.CloudPricing(provider="AWS", instance_type="m5.2xlarge",  vcpu=8,  ram_gb=32,  storage_gb=200, region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.2360,  monthly_cost=169.92),

    # 3yr-reserved
    models.CloudPricing(provider="AWS", instance_type="t3.medium",   vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0189,  monthly_cost=13.61),
    models.CloudPricing(provider="AWS", instance_type="m5.large",    vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0380,  monthly_cost=27.36),
    models.CloudPricing(provider="AWS", instance_type="m5.xlarge",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0760,  monthly_cost=54.72),

    # ─────────────────────────────────────────────
    # Azure — East US
    # ─────────────────────────────────────────────
    # on-demand
    models.CloudPricing(provider="Azure", instance_type="B1s",       vcpu=1,  ram_gb=1,   storage_gb=4,   region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0104,  monthly_cost=7.49),
    models.CloudPricing(provider="Azure", instance_type="B2s",       vcpu=2,  ram_gb=4,   storage_gb=8,   region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0416,  monthly_cost=29.95),
    models.CloudPricing(provider="Azure", instance_type="B4ms",      vcpu=4,  ram_gb=16,  storage_gb=32,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1660,  monthly_cost=119.52),
    models.CloudPricing(provider="Azure", instance_type="D2s_v3",    vcpu=2,  ram_gb=8,   storage_gb=16,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0960,  monthly_cost=69.12),
    models.CloudPricing(provider="Azure", instance_type="D4s_v3",    vcpu=4,  ram_gb=16,  storage_gb=32,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1920,  monthly_cost=138.24),
    models.CloudPricing(provider="Azure", instance_type="D8s_v3",    vcpu=8,  ram_gb=32,  storage_gb=64,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.3840,  monthly_cost=276.48),
    models.CloudPricing(provider="Azure", instance_type="D16s_v3",   vcpu=16, ram_gb=64,  storage_gb=128, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.7680,  monthly_cost=552.96),
    models.CloudPricing(provider="Azure", instance_type="F2s_v2",    vcpu=2,  ram_gb=4,   storage_gb=16,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0850,  monthly_cost=61.20),
    models.CloudPricing(provider="Azure", instance_type="E2s_v3",    vcpu=2,  ram_gb=16,  storage_gb=32,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1260,  monthly_cost=90.72),
    models.CloudPricing(provider="Azure", instance_type="E4s_v3",    vcpu=4,  ram_gb=32,  storage_gb=64,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.2520,  monthly_cost=181.44),

    # spot
    models.CloudPricing(provider="Azure", instance_type="D2s_v3",    vcpu=2,  ram_gb=8,   storage_gb=16,  region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0192,  monthly_cost=13.82),
    models.CloudPricing(provider="Azure", instance_type="D4s_v3",    vcpu=4,  ram_gb=16,  storage_gb=32,  region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0384,  monthly_cost=27.65),

    # 1yr-reserved
    models.CloudPricing(provider="Azure", instance_type="D2s_v3",    vcpu=2,  ram_gb=8,   storage_gb=16,  region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.0576,  monthly_cost=41.47),
    models.CloudPricing(provider="Azure", instance_type="D4s_v3",    vcpu=4,  ram_gb=16,  storage_gb=32,  region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.1152,  monthly_cost=82.94),
    models.CloudPricing(provider="Azure", instance_type="D8s_v3",    vcpu=8,  ram_gb=32,  storage_gb=64,  region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.2304,  monthly_cost=165.89),

    # 3yr-reserved
    models.CloudPricing(provider="Azure", instance_type="D2s_v3",    vcpu=2,  ram_gb=8,   storage_gb=16,  region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0384,  monthly_cost=27.65),
    models.CloudPricing(provider="Azure", instance_type="D4s_v3",    vcpu=4,  ram_gb=16,  storage_gb=32,  region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0768,  monthly_cost=55.30),

    # ─────────────────────────────────────────────
    # GCP — us-central1
    # ─────────────────────────────────────────────
    # on-demand
    models.CloudPricing(provider="GCP", instance_type="e2-micro",        vcpu=2,  ram_gb=1,   storage_gb=10,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0084,  monthly_cost=6.05),
    models.CloudPricing(provider="GCP", instance_type="e2-small",        vcpu=2,  ram_gb=2,   storage_gb=10,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0168,  monthly_cost=12.10),
    models.CloudPricing(provider="GCP", instance_type="e2-medium",       vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0335,  monthly_cost=24.12),
    models.CloudPricing(provider="GCP", instance_type="e2-standard-2",   vcpu=2,  ram_gb=8,   storage_gb=50,  region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0671,  monthly_cost=48.31),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-2",   vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.0971,  monthly_cost=69.91),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-4",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.1942,  monthly_cost=139.82),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-8",   vcpu=8,  ram_gb=32,  storage_gb=200, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.3883,  monthly_cost=279.58),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-16",  vcpu=16, ram_gb=64,  storage_gb=500, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.7766,  monthly_cost=559.15),
    models.CloudPricing(provider="GCP", instance_type="c2-standard-4",   vcpu=4,  ram_gb=16,  storage_gb=100, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.2088,  monthly_cost=150.34),
    models.CloudPricing(provider="GCP", instance_type="m1-megamem-96",   vcpu=8,  ram_gb=128, storage_gb=500, region="us-east", pricing_model="on-demand",    os="linux", price_per_hour=0.9000,  monthly_cost=648.00),

    # spot (preemptible)
    models.CloudPricing(provider="GCP", instance_type="e2-medium",       vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0067,  monthly_cost=4.82),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-2",   vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0233,  monthly_cost=16.78),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-4",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="spot",         os="linux", price_per_hour=0.0466,  monthly_cost=33.55),

    # 1yr-reserved (committed use)
    models.CloudPricing(provider="GCP", instance_type="n2-standard-2",   vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.0660,  monthly_cost=47.52),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-4",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.1320,  monthly_cost=95.04),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-8",   vcpu=8,  ram_gb=32,  storage_gb=200, region="us-east", pricing_model="1yr-reserved", os="linux", price_per_hour=0.2640,  monthly_cost=190.08),

    # 3yr-reserved
    models.CloudPricing(provider="GCP", instance_type="n2-standard-2",   vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0480,  monthly_cost=34.56),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-4",   vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.0960,  monthly_cost=69.12),
    models.CloudPricing(provider="GCP", instance_type="n2-standard-8",   vcpu=8,  ram_gb=32,  storage_gb=200, region="us-east", pricing_model="3yr-reserved", os="linux", price_per_hour=0.1920,  monthly_cost=138.24),

]

db.add_all(pricing_data)
db.commit()
db.close()
print(f"Database seeded successfully with {len(pricing_data)} records!")