import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
# we connected the supabase with sqlmodel

def init_db():
    SQLModel.metadata.create_all(engine)