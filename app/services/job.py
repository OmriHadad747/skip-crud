import json
import logging
import pydantic as pyd

from app.clients import redis
from app.schemas.job import Job, JobUpdate, JobStatusEnum
from app.schemas.response import MsgResp, EntityResp
from app.errors import Errors as err
from app.database.job import JobDB as db
from skip_common_lib.utils import custom_encoders as encoders


class CrudJob:
    logger = logging.getLogger("skip-crud-service")

    @classmethod
    @pyd.validate_arguments
    async def get_job_by_id(cls, id: str):
        cls.logger.debug(f"retrieveing job by id {id}")

        job = await db.get_job_by_id(id)
        if not job:
            return err.id_not_found(id)

        return EntityResp(output=dict(job=job))

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
        # add the new job into database
        res = await db.add_job(new_job)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(new_job.dict(exclude_none=True), op="insert")

        # push new job to new-jobs queue
        await redis.lpush(
            "new-jobs",
            json.dumps(new_job.dict(), default=encoders.custom_serializer),
        )

        return MsgResp(
            msg=f"{new_job.customer_email} new job {new_job.id} saved and pused to the queue",
        )

    @classmethod
    @pyd.validate_arguments
    async def update_job(cls, id: str, job: JobUpdate, status: JobStatusEnum):
        cls.logger.debug(f"udpating job {id} with fields {job.dict(exclude_none=True)}")

        res = await db.update_job(id, job, status)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(job.dict(exclude_none=True), op="update")

        return MsgResp(msg=f"job {id} updated in db")
