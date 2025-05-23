from sqlalchemy import Column, Integer, String
from app.database import Base

class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable = False)
    email = Column(String, index=True, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
