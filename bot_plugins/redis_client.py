from redis import Redis
import json
import os

redis = Redis(
    host=os.environ["REDIS_HOST"],
    port=os.environ["REDIS_PORT"],
    password=os.environ["REDIS_PASSWORD"],
)


def set_str(key, value):
    redis.set(key, value)


def get_str(key):
    value = redis.get(key)
    if value:
        return value.decode("utf-8")
    else:
        return ""


def set_dict(key, value):
    value = json.dumps(value)
    redis.set(key, value)


def get_dict(key):
    value = redis.get(key)
    if value:
        return json.loads(value.decode("utf-8"))
    else:
        return {}
