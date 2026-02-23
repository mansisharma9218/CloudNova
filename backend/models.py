from database import Base
from sqlalchemy import Column, Integer, String, Float

class CloudPricing(Base):
    __tablename__ = "cloud_pricing"

    id            = Column(Integer, primary_key=True, index=True)
    provider      = Column(String)   
    instance_type = Column(String)   
    vcpu          = Column(Integer)
    ram_gb        = Column(Float)
    storage_gb    = Column(Float)
    region        = Column(String)
    price_per_hour = Column(Float)