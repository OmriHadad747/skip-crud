from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from flask import current_app as app
from redis import Redis


redis = Redis(
    host=app.config["REDIS_HOST"],
    port=app.config["REDIS_PORT"],
    db=app.config["REDIS_DB"],
    decode_responses=True,
)
print(f"from queue {redis.rpop('new-jobs')}")

scheduler = APScheduler()

jwt = JWTManager()
