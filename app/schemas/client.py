from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic_settings import SettingsConfigDict

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str

class ClientUpdate(BaseModel):
    name: str
    email: EmailStr
    cpf: str

class ClientOut(ClientCreate):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)