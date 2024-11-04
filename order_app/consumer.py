from redis_client_2 import redis_client_2

key = "order_completed"
group = "inventory_group"

import time

try:
    redis_client_2.xgroup_create(
        key,
        group,
    )
except Exception as e:
    print("Group already exists")
    
# consumer
    while True:
        try:
            results = redis_client_2.xreadgroup(
                groupname=group,
                consumername=key,
                streams={key: ">"},
            )
            if results != []:
                for result in results:
                    for message in result[1]:
                        order = message[1]
                        print(order)
                        redis_client_2.xack(key, group, message[0])
        except Exception as e:
            print(str(e))
        time.sleep(1)
    