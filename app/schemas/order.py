from pydantic import EmailStr, BaseModel
from datetime import date
from typing import List
from pydantic_settings import SettingsConfigDict

class OrderItemCreate(BaseModel):
    product_id: int
    quantidade: int
    preco_unitario_no_pedido: float

class OrderCreate(BaseModel):
    numero_pedido: int
    data_pedido: date
    status: str = "Pendente"
    valor_total: float
    itens: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantidade: int
    preco_unitario_no_pedido: float

    model_config = SettingsConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    numero_pedido: int
    data_pedido: date
    status: str
    valor_total: float
    itens: List[OrderItemOut]

    model_config = SettingsConfigDict(from_attributes=True)
