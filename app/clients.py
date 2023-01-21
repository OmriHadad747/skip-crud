from aioredis import Redis

from app.settings import app_settings as s


redis = Redis.from_url(s.setting.redis_uri)
