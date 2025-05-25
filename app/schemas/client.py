from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str

class ClientOut(BaseModel):
    id: int

    class Config:
        orm_mode = True