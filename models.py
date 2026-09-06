from database import Base
from sqlalchemy import Column, String, Integer, Float

class ProduceListingTable(Base):
    __tablename__ = "listings"
    id = Column(String, primary_key=True)
    crop_type = Column(String)
    district = Column(String)
    quantity_quintals = Column(Integer)
    expected_price_per_quintal = Column(Float)
    grade = Column(String)
    farmer_name = Column(String)
    phone = Column(String)
    defect_percentage = Column(Float)
    uniformity_score = Column(Integer)

class BidTable(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)