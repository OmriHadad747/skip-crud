import json
import requests

from typing import Any, Dict
from flask import current_app as app
from app.utils import custom_json_encoder as json_enc
from app.extensions import scheduler, redis


@scheduler.task(trigger="interval", id="handle_new_jobs", seconds=10, max_instances=1)
def handle_new_jobs():
    with scheduler.app.app_context():
        new_job = redis.rpop("new-jobs")
        if not new_job:
            return

        new_job: Dict[str, Any] = json.loads(new_job)

        # post the job to freelancer-finder service
        url = f"http://{app.config['FREELANCER_FINDER_HOST']}/find"

        try:
            resp = requests.post(url, headers={"Content-Type": "application/json"}, json=new_job)

        except requests.exceptions.ConnectionError:
            app.logger.debug("lost connection with freelancer-finder service")
            redis.lpush("new-jobs", json.dumps(new_job, default=json_enc.custom_serializer))
            return

        if resp.status_code != 200:
            app.logger.debug(
                f"got {resp.status_code} from freelancer-finder service for job {new_job.get('id')}"
            )
            redis.lpush("new-jobs", json.dumps(new_job, default=json_enc.custom_serializer))
            return
