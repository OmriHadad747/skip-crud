import pydantic as pyd

from datetime import datetime
from enum import Enum
from bson import ObjectId

from app.schemas import CustomBaseModel


class JobCategoryEnum(Enum):
    GARAGE_DOOR = 0
    LOCK_SMITH = 1
    MOVING = 2


class JobStatusEnum(Enum):
    FREELANCER_FINDING = "freelancer finding"
    FREELANCER_FOUND = "freelancer found"
    FREELANCER_CANCELED = "freelancer canceled"
    CUSTOMER_CANCELD = "customer canceld"
    APPROVED = "customer approved"
    IN_PROGRESS = "in progress"
    DONE = "done"


class JobQuotation(CustomBaseModel):
    quotation_discription: str
    estimated_job_duration: str
    quotation: str


class Job(CustomBaseModel):
    created_at: datetime = pyd.Field(default_factory=datetime.now)
    id: str = pyd.Field(alias="_id", default_factory=ObjectId)
    category: JobCategoryEnum
    status: JobStatusEnum = JobStatusEnum.FREELANCER_FINDING.value
    description: str
    location: list[float] = pyd.Field(min_items=2, max_items=2)
    quotation: JobQuotation = None
    price: str = None
    customer_email: str
    customer_phone: str
    customer_address: str
    customer_county: str
    freelancer_email: str = None
    freelancer_phone: str = None

    @pyd.validator("id", pre=True)
    def convert_id_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class JobUpdate(CustomBaseModel):
    status: JobStatusEnum = None
    quotation: JobQuotation = None
    price: str = None
    freelancer_email: str = None
    freelancer_phone: str = None
