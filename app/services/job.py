import json

from typing import Any, Dict
from pydantic import validate_arguments
from flask import jsonify
from flask import current_app as app

from skip_common_lib.extensions import redis
from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.utils import custom_encoders as encoders
from skip_common_lib.models import job as job_model


class CrudJob:
    @classmethod
    @validate_arguments
    def post_job(cls, fields: Dict[str, Any]):
        # TODO write docstrings
        try:
            new_job = job_model.Job(**fields)
            redis.lpush(
                "new-jobs",
                json.dumps(new_job.dict(), default=encoders.custom_serializer),
            )

        except Exception as e:
            # TODO catch more specifiec exceptions
            return err.general_exception(e)

        app.logger.info(f"new job {new_job.id} pused to the queue")

        return (
            jsonify(msg=f"{new_job.customer_email} new job {new_job.id} post pused to the queue"),
            201,
        )
