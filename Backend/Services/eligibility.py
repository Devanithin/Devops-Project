from datetime import date, timedelta
from sqlalchemy.orm import Session
from models import Donor
from services.inventory_service import increase_stock

MIN_DAYS_GAP = 60

def process_donation(db: Session, donor_id: int):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise ValueError("Donor not found")

    if donor.last_donation_date:
        days_passed = (date.today() - donor.last_donation_date).days
        if days_passed < MIN_DAYS_GAP:
            raise ValueError(
                f"Not eligible. Wait {MIN_DAYS_GAP - days_passed} more days."
            )

    # Eligible → proceed
    donor.last_donation_date = date.today()
    increase_stock(db, donor.blood_type, units=1)

    db.commit()
    db.refresh(donor)
    return donor
