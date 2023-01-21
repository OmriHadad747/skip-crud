import json
import logging
import pydantic as pyd

from fastapi import status

from app.clients import redis
from app.schemas.job import Job, JobUpdate, JobStatusEnum
from app.schemas.response import MsgResp, EntityResp
from app.errors import Errors as err
from app.database.job import JobDB as db
from app.serializer import custom_json_serializer


class CrudJob:
    logger = logging.getLogger("crud-service")

    @classmethod
    @pyd.validate_arguments
    async def get_job_by_id(cls, id: str):
        cls.logger.debug(f"retrieveing job by id {id}")

        job = await db.get_job_by_id(id)
        if not job:
            return err.id_not_found(id)

        return EntityResp(entity=job)

    @classmethod
    @pyd.validate_arguments
    async def get_job_by_customer_email(cls, customer_email: str):
        pass

    @classmethod
    @pyd.validate_arguments
    async def get_job_by_freelancer_email(cls, freelancer_emial: str):
        pass

    @classmethod
    @pyd.validate_arguments
    async def add_job(cls, new_job: Job):
        cls.logger.info(f"adding job {new_job.id} to db and pushing in into 'new-jobs' queue")

        # add the new job into database
        res = await db.add_job(new_job)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(new_job.dict(exclude_none=True), op="insert")

        # push new job to new-jobs queue
        await redis.lpush(
            "new-jobs",
            json.dumps(new_job.dict(), default=custom_json_serializer),
        )

        return MsgResp(
            msg=f"{new_job.customer_email} new job {new_job.id} saved and pused to the queue",
        )

    @classmethod
    @pyd.validate_arguments
    async def update_and_return_job(cls, job_id: str, job: JobUpdate, job_status: JobStatusEnum):
        res = await db.update_job(job_id, job, curr_job_status=job_status)
        if res.matched_count == 0:
            cls.logger.debug(f"job {job_id} was not found")
            return MsgResp(msg=f"job {job_id} was not found. job status may changed").json_response(
                status_code=status.HTTP_404_NOT_FOUND
            )

        if not res.acknowledged:
            return err.db_op_not_acknowledged(job.dict(exclude_none=True), op="update")

        updated = await db.get_job_by_id(job_id)

        return EntityResp(msg=f"job {id} updated in db", entity=updated)

    @classmethod
    @pyd.validate_arguments
    async def update_job(
        cls, id: str, job: JobUpdate, job_status: JobStatusEnum, return_with_updated: bool = False
    ):
        cls.logger.debug(f"updating job {id} with fields {job.dict(exclude_none=True)}")

        if return_with_updated:
            return await cls.update_and_return_job(id, job, job_status)

        res = await db.update_job(id, job, curr_job_status=job_status)
        if res.matched_count == 0:
            cls.logger.debug(f"job {id} was not found")
            return MsgResp(msg=f"job {id} was not found. job status may changed").json_response(
                status_code=status.HTTP_404_NOT_FOUND
            )

        if not res.acknowledged:
            return err.db_op_not_acknowledged(job.dict(exclude_none=True), op="update")

        return MsgResp(msg=f"job {id} updated in db")
