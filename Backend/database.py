import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# This looks for your .env file and reads the DATABASE_URL
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# The engine is what actually connects to Supabase
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# This is a factory for creating database "sessions" (mini-connections)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This is the base class for all our tables (Donors, Inventory, etc.)
Base = declarative_base()
