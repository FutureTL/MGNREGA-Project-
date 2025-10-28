import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("GOV_RESOURCE_URL")
API_KEY = os.getenv("API_KEY")

async def fetch_mgnrega_data(state_name: str, district_name: str, fin_year: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                API_URL,
                params={
                    "filters[state_name]": state_name,
                    "filters[district_name]": district_name,
                    "filters[fin_year]": fin_year,
                    "api-key": API_KEY,
                    "format": "json"
                }
            )

            print("Status Code:", response.status_code)
            print("Response Text:", response.text)  # limit print length

            response.raise_for_status()
            data = response.json()
            return data

    except Exception as e:
        print(f"API failed to fetch: {e}")
        return None
