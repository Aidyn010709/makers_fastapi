from datetime import datetime


def validate_date(date: datetime):
    aware_dt = None
    if date:
        aware_dt = date.replace(tzinfo=None)
    else:
        raise ValueError("Deadline not defined")
    return aware_dt
