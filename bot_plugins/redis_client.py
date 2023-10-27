from redis import Redis
import json
import os

redis = Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ["REDIS_PASSWORD"],
)


def set_dict(key, value):
    value = json.dumps(value)
    redis.set(key, value)


def get_dict(key):
    value = redis.get(key)
    if value:
        value = value.decode("utf-8")
        return json.loads(value)
    else:
        return {}
