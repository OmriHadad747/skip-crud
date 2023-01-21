import pydantic as pyd

from app.schemas import CustomBaseModel
from app.schemas.job import JobCategoryEnum


class NearestFilterReq(CustomBaseModel):
    job_location: list[float] = pyd.Field(min_items=2, max_items=2)
    job_category: JobCategoryEnum
    customer_county: str
