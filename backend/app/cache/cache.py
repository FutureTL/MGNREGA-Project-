import json
from app.cache.connection import redis  # import the client you made in connection.py

# Save data in cache
async def set_cache_data(key: str, value, expire_seconds: int = 86400):
    data = json.dumps(value)
    redis.set(key, data, ex=expire_seconds)  # async version of set
    print("the data is cached")

# Retrieve data from cache
async def get_cache_data(key: str):
    data =  redis.get(key)
    if data:
        print(f"cached data is being returned: {key}")
        return json.loads(data)
    return None