from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from pydantic_settings import SettingsConfigDict

class ProductCreate(BaseModel):
    descricao: str
    valor_venda: float
    EAN: Optional[int] = None
    secao: str
    estoque_inicial: Optional[int] = None
    validade: Optional[date] = None
    imagem_url: Optional[str] = None

class ProductOut(ProductCreate):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)
