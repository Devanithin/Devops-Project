from sqlalchemy.orm import Session
from models import Inventory

def increase_stock(db: Session, blood_type: str, units: int = 1):
    inventory = db.query(Inventory).filter_by(blood_type=blood_type).first()
    if not inventory:
        inventory = Inventory(blood_type=blood_type, units_available=0)
        db.add(inventory)
    inventory.units_available += units
    return inventory

def decrease_stock(db: Session, blood_type: str, units: int = 1):
    inventory = db.query(Inventory).filter_by(blood_type=blood_type).first()
    if not inventory or inventory.units_available < units:
        raise ValueError("Insufficient stock")
    inventory.units_available -= units
    return inventory
