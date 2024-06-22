import datetime
import enum
import pytz
from datetime import datetime

from typing import Any
from pydantic import BaseModel
from passlib.context import CryptContext

from makers.config.settings import settings


TZ = pytz.timezone(settings.TZ)


def get_current_time() -> datetime:
    return datetime.now(tz=TZ).replace(tzinfo=None)


class RolesEnum(enum.Enum):
    user = "USER"
    company = "COMPANY"
    admin = "ADMIN"


class RequestStatus(enum.Enum):
    waiting = "WAITING"
    accepted = "ACCEPTED"
    canceled = "CANCELED"


class Weekdays(enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Constants(BaseModel):
    PWD_CONTEXT: Any = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # auth errors
    INVALID_TOKEN: str = "Invalid Token"
    INVALID_AUTH_DATA: str = "Incorrect Email or Password"
    ONLY_ADMIN: str = "Only admin users have access"

    # not found
    COMPANY_NOT_FOUND: str = "Company not found"
    USER_NOT_FOUND: str = "User not found"
    TEAM_NOT_FOUND: str = "Team not found"
    MEMBER_NOT_FOUND: str = "Member not found"
    INTERNSHIP_NOT_FOUND: str = "Internship not found"
    INTERNSHIP_PAYMENT_NOT_FOUND: str = "Internship payment not found"
    INTERNSHIP_MEMBER_NOT_FOUND: str = "Internship member not found"
    SUBSCRIPTION_NOT_FOUND: str = "Subscription not found"
    INTERVIEW_PAYMENT_NOT_FOUND: str = "Interview payment not found"
    NO_DIRECTION: str = "No Direction"

    # constraints
    ALL_DELETE: str = "all, delete"

    # mailjet constants
    SENDER_EMAIL: str = "makersincubator@gmail.com"
    SENDER_NAME: str = "Juniors.dev"
    MAILJET_GREETING: str = "Greetings from Mailjet!"

    # IDs
    USER_ID: str = "User ID"
    COMPANY_ID: str = "Company ID"
    IR_ID: str = "Interview Request ID"
    IP_ID: str = "Internship Programme ID"
    IR_MODAL_DESC_ID: str = "IR Modal Description ID"
    FAQ_ID: str = "FAQ ID"


CONSTANTS = Constants()

EMPTY_VALUES = ([], (), {}, "", None)

ALLOWED_TYPES = [
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/heic",
    "image/svg",
    "application/octet-stream",
]
