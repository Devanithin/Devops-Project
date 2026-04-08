from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import BloodRequest, Donor, NotificationLog
from pydantic import BaseModel
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

router = APIRouter()

class BloodRequestCreate(BaseModel):
    hospital_id: int
    blood_type: str
    units_needed: int
    patient_name: str
    accident_location: str

class DonorResponse(BaseModel):
    donor_id: int
    response: str

def get_prioritized_donors(accident_lat, accident_lon, blood_type, db):
    donors = db.query(Donor).filter(
        Donor.blood_type == blood_type,
        Donor.is_available == True
    ).all()

    scored = []
    for donor in donors:
        distance = geodesic(
            (accident_lat, accident_lon),
            (donor.latitude, donor.longitude)
        ).km
        days_since_active = (datetime.utcnow() - donor.last_active).days
        score = (distance * 0.5) + (days_since_active * 0.3)
        scored.append((score, distance, donor))

    scored.sort(key=lambda x: x[0])
    return scored

@router.post("/create")
def create_blood_request(request: BloodRequestCreate, db: Session = Depends(get_db)):
    geolocator = Nominatim(user_agent="blood_donor_system")
    location = geolocator.geocode(request.accident_location + ", India")

    if not location:
        raise HTTPException(status_code=400, detail="Could not find accident location.")

    new_request = BloodRequest(
        hospital_id=request.hospital_id,
        blood_type=request.blood_type,
        units_needed=request.units_needed,
        patient_name=request.patient_name,
        accident_latitude=location.latitude,
        accident_longitude=location.longitude,
        status="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    prioritized = get_prioritized_donors(
        location.latitude,
        location.longitude,
        request.blood_type,
        db
    )

    notified = []
    for score, distance, donor in prioritized[:5]:
        log = NotificationLog(
            request_id=new_request.id,
            donor_id=donor.id,
            status="sent"
        )
        db.add(log)
        notified.append({
            "donor_id": donor.id,
            "name": donor.name,
            "phone": donor.phone,
            "distance_km": round(distance, 2)
        })

    db.commit()
    return {
        "message": "Blood request created",
        "request_id": new_request.id,
        "accident_location": location.address,
        "donors_notified": notified
    }

@router.get("/all")
def get_all_requests(db: Session = Depends(get_db)):
    requests = db.query(BloodRequest).all()
    return requests

@router.get("/{request_id}")
def get_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.post("/{request_id}/respond")
def donor_respond(request_id: int, response: DonorResponse, db: Session = Depends(get_db)):
    log = db.query(NotificationLog).filter(
        NotificationLog.request_id == request_id,
        NotificationLog.donor_id == response.donor_id
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Notification not found")

    log.donor_response = response.response
    log.responded_at = datetime.utcnow()
    log.status = response.response

    if response.response == "accepted":
        req = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
        req.status = "accepted"

    db.commit()
    return {"message": f"Response recorded: {response.response}"}

@router.get("/{request_id}/donors")
def get_notified_donors(request_id: int, db: Session = Depends(get_db)):
    logs = db.query(NotificationLog).filter(
        NotificationLog.request_id == request_id
    ).all()
    return logs