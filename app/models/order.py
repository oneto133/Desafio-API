from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.product import Products

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index = True)
    numero_pedido = Column(Integer, unique=True, nullable=False)
    data_pedido = Column(Date, nullable=False)
    status = Column(String(50), nullable=False, default="Pendente")
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    itens = relationship("OrderItem", back_populates="pedido")

    def __repr__(self):
        return f"<Order(id={self.id}, numero_pedido= '{self.numero_pedido}')>"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario_no_pedido = Column(DECIMAL(10,2), nullable=False)

    pedido = relationship("Orders", back_populates="itens")
    produto = relationship("Products")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantidade={self.quantidade})>"