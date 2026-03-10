from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from .database import Base
class Donor(Base):
   __tablename__ = "donors"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, nullable=False)
   blood_type = Column(String, nullable=False)
   phone = Column(String)
   last_donation_date = Column(Date)
class Inventory(Base):
   __tablename__ = "inventory"
   id = Column(Integer, primary_key=True, index=True)
   blood_type = Column(String, unique=True, index=True)
   units_available = Column(Integer, default=0)
   updated_at = Column(DateTime(timezone=True), on_server_default=func.now())
