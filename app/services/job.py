import json
import logging

from app.clients import redis
from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.utils import custom_encoders as encoders
from skip_common_lib.schemas import job as job_schema
from skip_common_lib.schemas import response as resp_schemas


class CrudJob:
    logger = logging.getLogger("skip-crud-service")

    @classmethod
    def post_job(cls, new_job: job_schema.Job):
        # TODO make async after setting redis async client

        try:
            redis.lpush(
                "new-jobs",
                json.dumps(new_job.dict(), default=encoders.custom_serializer),
            )

        except Exception as e:
            # TODO catch more specifiec exceptions
            return err.general_exception(e, cls.logger)

        cls.logger.info(f"new job {new_job.id} pused to the queue")

        return resp_schemas.MsgResponse(
            args=json.loads(json.dumps(new_job.dict(), default=encoders.custom_serializer)),
            msg=f"{new_job.customer_email} new job {new_job.id} post pused to the queue",
        )
