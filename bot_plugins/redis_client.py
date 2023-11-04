from redis import Redis
import pickle
import os

redis = Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ["REDIS_PASSWORD"],
)


def set_dict(key, value):
    value = pickle.dumps(value)
    redis.set(key, value)


def get_dict(key):
    value = redis.get(key)
    if value:
        return pickle.loads(value)
    else:
        return {"current": "not_found"}
