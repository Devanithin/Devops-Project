from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Donor
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from geopy.geocoders import Nominatim

router = APIRouter()

class DonorCreate(BaseModel):
    name: str
    phone: str
    email: str
    blood_type: str
    city: str
    address: str

class DonorUpdate(BaseModel):
    is_available: Optional[bool] = None
    city: Optional[str] = None
    address: Optional[str] = None

@router.post("/register")
def register_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    existing = db.query(Donor).filter(Donor.phone == donor.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered")

    geolocator = Nominatim(user_agent="blood_donor_system")
    location = geolocator.geocode(donor.address + ", " + donor.city + ", India")

    if not location:
        raise HTTPException(status_code=400, detail="Could not find location. Please be more specific.")

    new_donor = Donor(
        name=donor.name,
        phone=donor.phone,
        email=donor.email,
        blood_type=donor.blood_type,
        city=donor.city,
        latitude=location.latitude,
        longitude=location.longitude,
        last_active=datetime.utcnow()
    )
    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return {
        "message": "Donor registered successfully",
        "donor_id": new_donor.id,
        "location_detected": location.address,
        "coordinates": {"lat": location.latitude, "lon": location.longitude}
    }

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

    if update.address and update.city:
        geolocator = Nominatim(user_agent="blood_donor_system")
        location = geolocator.geocode(update.address + ", " + update.city + ", India")
        if location:
            donor.latitude = location.latitude
            donor.longitude = location.longitude

    if update.is_available is not None:
        donor.is_available = update.is_available
    if update.city:
        donor.city = update.city

    donor.last_active = datetime.utcnow()
    db.commit()
    return {"message": "Donor updated successfully"}