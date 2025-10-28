from ast import AST
from zoneinfo import ZoneInfo
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta, timezone


class MGNREGAData(SQLModel, table=True):
    id: Optional[int]= Field(default=None, primary_key= True)
    state_name: str
    district_name: str
    fin_year= str
    data_json:str
    created_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))
    
