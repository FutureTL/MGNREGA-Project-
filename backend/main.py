from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from app.core.db import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.services.gov_api import get_mgnrega_data
from app.dataprocessing.data_processing import preprocess_mgnrega_data
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
# code written before yield runs on startup

app= FastAPI(title= "MGNREGA Project")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow all HTTP methods
    allow_headers=["*"],   # allow all headers
)


@app.get("/fetch_api_data")
async def fetch_data(state_name:str,district_name: str, fin_year: Optional[str] = None):
    if not fin_year:
        now = datetime.now()
        fin_year = f"{now.year - 1}-{now.year}"
    
    data= await get_mgnrega_data(state_name, district_name, fin_year)
    print(f"data recieved from get_mgnerga_data: {data}")
    if data:
        processed_data= preprocess_mgnrega_data(data)
        print(f"processed_data: {processed_data}")
        return {"status": "success", "data": processed_data}
    
    else:
        return {"status": "error", "message": "data could not be fetched"}


@app.get("/")
async def health():
    return {"status": "ok", "message": "Backend running!"}