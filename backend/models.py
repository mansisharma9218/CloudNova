from database import Base
from sqlalchemy import Column, Integer, String, Float

class CloudPricing(Base):
    __tablename__ = "cloud_pricing"

    id             = Column(Integer, primary_key=True, index=True)
    provider       = Column(String)    # AWS, Azure, GCP
    instance_type  = Column(String)    # t3.medium, B2s, e2-medium
    vcpu           = Column(Integer)
    ram_gb         = Column(Float)
    storage_gb     = Column(Float)
    region         = Column(String)    # us-east, us-west, europe, asia
    pricing_model  = Column(String)    # on-demand, 1yr-reserved, 3yr-reserved, spot
    os             = Column(String)    # linux (default)
    price_per_hour = Column(Float)
    monthly_cost   = Column(Float)