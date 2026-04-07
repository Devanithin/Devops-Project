from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Hospital, BloodInventory
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class HospitalCreate(BaseModel):
    name: str
    city: str
    phone: str
    latitude: float
    longitude: float

class InventoryUpdate(BaseModel):
    blood_type: str
    units_available: int

@router.post("/register")
def register_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    new_hospital = Hospital(**hospital.model_dump())
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return {"message": "Hospital registered successfully", "hospital_id": new_hospital.id}

@router.get("/all")
def get_all_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).all()
    return hospitals

@router.get("/{hospital_id}")
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@router.post("/{hospital_id}/inventory")
def update_inventory(hospital_id: int, inventory: InventoryUpdate, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    existing = db.query(BloodInventory).filter(
        BloodInventory.hospital_id == hospital_id,
        BloodInventory.blood_type == inventory.blood_type
    ).first()
    if existing:
        existing.units_available = inventory.units_available
        existing.updated_at = datetime.utcnow()
    else:
        new_inv = BloodInventory(
            hospital_id=hospital_id,
            blood_type=inventory.blood_type,
            units_available=inventory.units_available
        )
        db.add(new_inv)
    db.commit()
    return {"message": "Inventory updated successfully"}

@router.get("/{hospital_id}/inventory")
def get_inventory(hospital_id: int, db: Session = Depends(get_db)):
    inventory = db.query(BloodInventory).filter(
        BloodInventory.hospital_id == hospital_id
    ).all()
    return inventory