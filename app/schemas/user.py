from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    senha: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    role: str

    class Config:
        orm_mode = True