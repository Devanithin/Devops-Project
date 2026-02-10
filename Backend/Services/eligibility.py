from datetime import date, timedelta
from models import Donor

MIN_DAYS_GAP = 60

def is_donor_eligible(donor: Donor) -> tuple[bool, int]:
    if donor.last_donation_date is None:
        return True, 0

    days_passed = (date.today() - donor.last_donation_date).days
    if days_passed >= MIN_DAYS_GAP:
        return True, 0

    return False, MIN_DAYS_GAP - days_passed
