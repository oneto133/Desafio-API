from pydantic import EmailStr, BaseModel
from datetime import date
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantidade: int
    preco_unitario_no_pedido: float

class OrderCreate(BaseModel):
    numero_pedido: int
    data_pedido: date
    status: str = "Pendente"
    valor_total = float
    itens = List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantidade: int
    preco_unitario_no_pedido: float

    class Config:
        orm_mode= True

class OrderOut(BaseModel):
    id: int
    numero_pedido: int
    data_pedido: date
    status: str
    valor_total: float
    itens: List[OrderItemOut]

    class Config():
        orm_mode= True
