from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("url", "postgresql://user:passwor")