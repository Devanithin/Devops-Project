from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Donor
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class DonorCreate(BaseModel):
    name: str
    phone: str
    email: str
    blood_type: str
    latitude: float
    longitude: float
    city: str

class DonorUpdate(BaseModel):
    is_available: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None

@router.post("/register")
def register_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    existing = db.query(Donor).filter(Donor.phone == donor.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered")
    new_donor = Donor(**donor.model_dump(), last_active=datetime.utcnow())
    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return {"message": "Donor registered successfully", "donor_id": new_donor.id}

@router.get("/all")
def get_all_donors(db: Session = Depends(get_db)):
    donors = db.query(Donor).all()
    return donors

@router.get("/{donor_id}")
def get_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor

@router.put("/{donor_id}/update")
def update_donor(donor_id: int, update: DonorUpdate, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    for key, value in update.model_dump(exclude_none=True).items():
        setattr(donor, key, value)
    donor.last_active = datetime.utcnow()
    db.commit()
    return {"message": "Donor updated successfully"}