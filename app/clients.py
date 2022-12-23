from redis import Redis

from skip_common_lib.settings import app_settings as s


redis = Redis.from_url(s.setting.redis_uri)
# TODO find a better way to clear the queue
print(f"from queue {redis.rpop('new-jobs')}")  