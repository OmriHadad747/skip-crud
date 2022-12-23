import json
import requests
import logging

from typing import Any, Dict
from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every

from app.clients import redis
from skip_common_lib.settings import app_settings as s
from skip_common_lib.utils import custom_encoders as encoders


logger = logging.getLogger("skip-crud-service")
scheduler = APIRouter()


@scheduler.on_event("startup")
@repeat_every(seconds=5)
def handle_new_jobs_task():
    new_job = redis.rpop("new-jobs")
    if not new_job:
        return

    new_job: Dict[str, Any] = json.loads(new_job)

    # post the job to freelancer-finder service
    url = f"http://{s.setting.freelancer_finder_url}/find"

    try:
        resp = requests.post(url, headers={"Content-Type": "application/json"}, json=new_job)

    except requests.exceptions.ConnectionError:
        logger.debug("lost connection with freelancer-finder service")
        redis.lpush("new-jobs", json.dumps(new_job, default=encoders.custom_serializer))
        return

    if resp.status_code != 200:
        logger.debug(
            f"got {resp.status_code} from freelancer-finder service for job {new_job.get('id')}"
        )
        redis.lpush("new-jobs", json.dumps(new_job, default=encoders.custom_serializer))
        return
