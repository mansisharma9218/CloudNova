from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

pricing_data = [
    models.CloudPricing(provider="AWS",   instance_type="t3.micro",      vcpu=2,  ram_gb=1,   storage_gb=20,  region="us-east-1",    price_per_hour=0.0104),
    models.CloudPricing(provider="AWS",   instance_type="t3.medium",     vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-east-1",    price_per_hour=0.0416),
    models.CloudPricing(provider="AWS",   instance_type="m5.large",      vcpu=2,  ram_gb=8,   storage_gb=100, region="us-east-1",    price_per_hour=0.0960),
    models.CloudPricing(provider="AWS",   instance_type="m5.xlarge",     vcpu=4,  ram_gb=16,  storage_gb=200, region="us-east-1",    price_per_hour=0.1920),
    models.CloudPricing(provider="Azure", instance_type="B2s",           vcpu=2,  ram_gb=4,   storage_gb=50,  region="eastus",       price_per_hour=0.0416),
    models.CloudPricing(provider="Azure", instance_type="D2s_v3",        vcpu=2,  ram_gb=8,   storage_gb=100, region="eastus",       price_per_hour=0.0960),
    models.CloudPricing(provider="Azure", instance_type="D4s_v3",        vcpu=4,  ram_gb=16,  storage_gb=200, region="eastus",       price_per_hour=0.1920),
    models.CloudPricing(provider="GCP",   instance_type="e2-micro",      vcpu=2,  ram_gb=1,   storage_gb=20,  region="us-central1",  price_per_hour=0.0084),
    models.CloudPricing(provider="GCP",   instance_type="e2-medium",     vcpu=2,  ram_gb=4,   storage_gb=50,  region="us-central1",  price_per_hour=0.0335),
    models.CloudPricing(provider="GCP",   instance_type="n2-standard-2", vcpu=2,  ram_gb=8,   storage_gb=100, region="us-central1",  price_per_hour=0.0971),
    models.CloudPricing(provider="GCP",   instance_type="n2-standard-4", vcpu=4,  ram_gb=16,  storage_gb=200, region="us-central1",  price_per_hour=0.1942),
]

db.add_all(pricing_data)
db.commit()
db.close()
print(" Database seeded successfully!")