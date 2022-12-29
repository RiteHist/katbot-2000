import redis
import json


def create_connection(db: int) -> redis.Redis:
    return redis.Redis(host='redis', db=db)


def put_data(data: dict, db: int, key: str) -> bool:
    r = create_connection(db)
    return r.set(key, json.dumps(data))


def get_data(db: int, key: str) -> dict:
    r = create_connection(db)
    data = r.get(key)
    if data:
        return json.loads(data)
    return {}
