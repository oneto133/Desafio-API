from sqlalchemy import Column, Integer, String, Date, DECIMAL
from app.database import Base

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    descrição = Column(String, nullable=False)
    valor_venda = Column(DECIMAL(10,2), nullable=False, index=True)
    EAN = Column(Integer, unique=True, nullable=True)
    seção = Column(String, nullable=False)
    estoque_inicial = Column(Integer, nullable=True)
    Validade = Column(Date, nullable=True, unique=False, index=True)
    Imagem_url = Column(String, nullable=True, index=True)

    def __repr__(self):
        return f"<Product(id={self.id}, descrição='{self.descrição}')>"