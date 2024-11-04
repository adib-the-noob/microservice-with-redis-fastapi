from redis_om import get_redis_connection

redis_client_2 = get_redis_connection(
    host="localhost",
    port=6380,
    db=0,
    decode_responses=True
)