from motor import motor_asyncio
from bson.codec_options import TypeEncoder, TypeRegistry, CodecOptions

from app.schemas.job import JobCategoryEnum, JobStatusEnum
from app.schemas.freelancer import FreelancerStatusEnum
from app.settings import app_settings as s


db: motor_asyncio.AsyncIOMotorDatabase = motor_asyncio.AsyncIOMotorClient(f"{s.setting.mongo_uri}")[
    s.setting.db_name
]
_freelancers = s.setting.freelancers_collection_name
_customers = s.setting.customers_collection_name
_jobs = s.setting.jobs_collection_name


class JobCategoryEncoder(TypeEncoder):

    python_type = JobCategoryEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


job_category_encoder = JobCategoryEncoder()


class JobStatusEncoder(TypeEncoder):

    python_type = JobStatusEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


job_status_encoder = JobStatusEncoder()


class FreelancertatusEncoder(TypeEncoder):

    python_type = FreelancerStatusEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


freelancer_status_encoder = FreelancertatusEncoder()


codec_options = CodecOptions(
    type_registry=TypeRegistry(
        [job_category_encoder, job_status_encoder, freelancer_status_encoder]
    )
)
