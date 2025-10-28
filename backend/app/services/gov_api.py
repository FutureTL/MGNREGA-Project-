# we will handle communication with gov api,
# first we will check the cache , if not found there or stale then
# we query the gov api.
# in querying the gov api if that fails then stale cache has to be returned.
import os
from typing import Optional
from dotenv import load_dotenv
from app.cache.cache import get_cache_data, set_cache_data
from datetime import datetime, timedelta
from app.services.client_api import fetch_mgnrega_data

load_dotenv()

GOV_RESOURCE = os.getenv("GOV_RESOURCE_URL")
API_KEY = os.getenv("API_KEY")

# CACHE_TTL = 60*60*24
CACHE_EXPIRY_SECONDS = 86400
STALE_CACHE_TOLERANCE = timedelta(days=2)

async def get_mgnrega_data(state_name:str,district_name:str, fin_year:Optional[str]=None):

    cache_key =f"{state_name}_{district_name}_{fin_year}"

    cache_data = await get_cache_data(cache_key)
    if cache_data:
        print("cache hit")
        cached_time = datetime.fromisoformat(cache_data.get("timestamp", datetime.now().isoformat()))
        if datetime.now()- cached_time < STALE_CACHE_TOLERANCE:
            print("cache is fresh, returning data from it")
            return cache_data["data"]
        else: 
            print("Cache is old, will refresh from API if possible.")

    
    api_data = await fetch_mgnrega_data(state_name, district_name, fin_year)
    if api_data:
        print("api call successful, also updating cache")
        await set_cache_data(cache_key, {
            "timestamp":  datetime.now().isoformat(),
            "data":api_data
        },expire_seconds= CACHE_EXPIRY_SECONDS)
        return api_data
        
        
# step -3 if cache is old but api data couldn't be fetched:
    elif cache_data:
            print("api failed and returning old cache data")
            return cache_data["data"]
    
# step -4 no cache and no api fetch possible
    else:
        return {"status": "error", "message": "No data available from API or cache"}
    
    
    
    # params={
    #     "api-key": API_KEY,
    #     "format":"json",
    #     "limit":10,
    #     "filters[state_name]": state_name,
    #     "filters[district_name]": district_name,
    #     "filters[fin_year]": fin_year
    # }

    # async with httpx.AsyncClient(timeout=10.0) as client:
    #     response = await client.get(GOV_RESOURCE, params=params)
    #     response.raise_for_status()
    #     data = response.json()
    #     print("data received from gov api")
    
    # redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
    # print("data received from gov- added to cache")
    # return data