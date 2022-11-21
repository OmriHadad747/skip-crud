import json

from typing import Any, Dict
from pydantic import validate_arguments
from flask import jsonify
from flask import current_app as app
from app.extensions import redis
from app.utils.errors import Errors as err
from app.utils import custom_json_encoder as json_enc
from skip_db_lib.models import job as job_model


class CrudJob:
    @classmethod
    @validate_arguments
    def post_job(cls, fields: Dict[str, Any]):
        # TODO write docstrings
        try:
            new_job = job_model.Job(**fields)
            redis.lpush(
                "new-jobs",
                json.dumps(new_job.dict(), default=json_enc.custom_serializer),
            )

        except Exception as e:
            # TODO catch more specifiec exceptions
            return err.general_exception(e)

        app.logger.info(f"new job {new_job.id} pused to the queue")

        return (
            jsonify(msg=f"{new_job.customer_email} new job {new_job.id} post pused to the queue"),
            201,
        )
