from datetime import datetime, date
from bson import ObjectId

from app.schemas.job import JobStatusEnum, JobCategoryEnum


def custom_json_serializer(obj):
    """
    JSON serializer for objects not serializable by default
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, (JobStatusEnum, JobCategoryEnum)):
        return obj.value
    elif isinstance(obj, ObjectId):
        return str(obj)