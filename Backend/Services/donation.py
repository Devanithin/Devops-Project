from datetime import date
from sqlalchemy.orm import Session
from models import Donor
from services.eligibility_service import is_donor_eligible
from services.inventory_service import increase_stock

def process_donation(db: Session, donor_id: int):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise ValueError("Donor not found")

    eligible, wait_days = is_donor_eligible(donor)
    if not eligible:
        raise ValueError(f"Not eligible. Wait {wait_days} more days.")

    donor.last_donation_date = date.today()
    increase_stock(db, donor.blood_type, units=1)

    db.commit()
    db.refresh(donor)
    return donor
