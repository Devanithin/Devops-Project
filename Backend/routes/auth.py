from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Donor, Hospital
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token
from geopy.geocoders import Nominatim
from datetime import datetime

router = APIRouter()

class DonorRegister(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    blood_type: str
    city: str
    address: str

class HospitalRegister(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    city: str
    address: str

class LoginRequest(BaseModel):
    phone: str
    password: str

@router.post("/register/donor")
def register_donor(donor: DonorRegister, db: Session = Depends(get_db)):
    if db.query(Donor).filter(Donor.phone == donor.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")
    if db.query(Donor).filter(Donor.email == donor.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    geolocator = Nominatim(user_agent="blood_donor_system")
    location = geolocator.geocode(donor.address + ", " + donor.city + ", India")
    if not location:
        raise HTTPException(status_code=400, detail="Could not find location. Be more specific.")

    new_donor = Donor(
        name=donor.name,
        phone=donor.phone,
        email=donor.email,
        hashed_password=hash_password(donor.password),
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
        "location_detected": location.address
    }
#geognaeerioh
@router.post("/register/hospital")
def register_hospital(hospital: HospitalRegister, db: Session = Depends(get_db)):
    if db.query(Hospital).filter(Hospital.phone == hospital.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")
    if db.query(Hospital).filter(Hospital.email == hospital.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    geolocator = Nominatim(user_agent="blood_donor_system")
    location = geolocator.geocode(hospital.address + ", " + hospital.city + ", India")
    if not location:
        raise HTTPException(status_code=400, detail="Could not find location. Be more specific.")

    new_hospital = Hospital(
        name=hospital.name,
        phone=hospital.phone,
        email=hospital.email,
        hashed_password=hash_password(hospital.password),
        city=hospital.city,
        latitude=location.latitude,
        longitude=location.longitude
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return {
        "message": "Hospital registered successfully",
        "hospital_id": new_hospital.id,
        "location_detected": location.address
    }

@router.post("/login/donor")
def login_donor(credentials: LoginRequest, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.phone == credentials.phone).first()
    if not donor or not verify_password(credentials.password, donor.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid phone or password")

    token = create_access_token({"donor_id": donor.id, "role": "donor"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "donor",
        "donor_id": donor.id,
        "name": donor.name,
        "blood_type": donor.blood_type
    }

@router.post("/login/hospital")
def login_hospital(credentials: LoginRequest, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.phone == credentials.phone).first()
    if not hospital or not verify_password(credentials.password, hospital.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid phone or password")

    token = create_access_token({"hospital_id": hospital.id, "role": "hospital"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "hospital",
        "hospital_id": hospital.id,
        "name": hospital.name
    }