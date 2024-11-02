from redis_om import get_redis_connection

redis_client = get_redis_connection(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
