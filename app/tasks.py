import json
import logging

from typing import Any, Dict
from fastapi import APIRouter
from fastapi import status
from fastapi_utils.tasks import repeat_every
from httpx import _exceptions as httpx_exc

from app.clients import redis
from app.settings import app_settings as s
from skip_common_lib.utils import custom_encoders as encoders
from skip_common_lib.utils.async_http import AsyncHttp
from skip_common_lib.consts import HttpMethod


logger = logging.getLogger("skip-crud-service")
scheduler = APIRouter()


@scheduler.on_event("startup")
@repeat_every(seconds=30)
async def handle_new_jobs_task():
    new_job = redis.rpop("new-jobs")
    if not new_job:
        return

    new_job: Dict[str, Any] = json.loads(new_job)

    try:
        # post the job to freelancer-finder service
        resp = AsyncHttp.http_call(
            method=HttpMethod.POST, url=f"{s.setting.freelancer_finder_url}/find", json=new_job
        )

    except httpx_exc.HTTPError:
        logger.error("lost connection with freelancer-finder service")
        await redis.lpush("new-jobs", json.dumps(new_job, default=encoders.custom_serializer))
        return

    if resp.status_code != status.HTTP_200_OK:
        logger.error(
            f"got {resp.status_code} from freelancer-finder service for job {new_job.get('id')}"
        )
        await redis.lpush("new-jobs", json.dumps(new_job, default=encoders.custom_serializer))
