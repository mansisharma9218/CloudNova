from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import CloudPricing
from auth import verify_token

router = APIRouter()

@router.get("/")
def get_pricing(
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):
    pricing = db.query(CloudPricing).all()
    return [
        {
            "id": p.id,
            "provider": p.provider,
            "instance": p.instance_type,
            "vcpu": p.vcpu,
            "ram": p.ram_gb,
            "storage_gb": p.storage_gb,
            "region": p.region,
            "price": p.price_per_hour,
        }
        for p in pricing
    ]


@router.get("/{provider}")
def get_pricing_by_provider(
    provider: str,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
):
    pricing = db.query(CloudPricing).filter(
        CloudPricing.provider == provider.upper()
    ).all()

    return [
        {
            "id": p.id,
            "provider": p.provider,
            "instance": p.instance_type,
            "vcpu": p.vcpu,
            "ram": p.ram_gb,
            "storage_gb": p.storage_gb,
            "region": p.region,
            "price": p.price_per_hour,
        }
        for p in pricing
    ]