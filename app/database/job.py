from typing import Any
from bson import ObjectId
from pymongo import collection, results

from app.schemas.job import Job, JobUpdate, JobStatusEnum
from app.database import db, _jobs
from app.database import codec_options


class JobDB:
    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion.

        Returns:
            collection.Collection: Jobs collection.
        """
        return db[_jobs].with_options(codec_options=codec_options)

    @classmethod
    async def get_job_by_id(cls, id: str) -> dict[str, Any]:
        job = await cls._get_coll().find_one({"_id": ObjectId(id)})
        return job

    @classmethod
    async def add_job(cls, job: Job) -> results.InsertOneResult:
        result = await cls._get_coll().insert_one(job.dict(by_alias=True))
        return result

    @classmethod
    async def update_job(
        cls, id: str, job: JobUpdate, curr_job_status: JobStatusEnum
    ) -> results.UpdateResult:
        result = await cls._get_coll().update_one(
            {"_id": ObjectId(id), "status": curr_job_status.value},
            {"$set": job.dict(exclude_none=True)},
        )

        return result
