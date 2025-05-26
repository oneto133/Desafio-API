from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Products(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Products).filter(models.Products.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10, secao: str = None):
    query = db.query(models.Products)
    if secao:
        query = query.filter(models.Products.secao.ilike(f"%{secao}%"))
    return query.offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for field, value in product.dict().items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(db_product)
    db.commit()
    return {"detail": "Produto deletado com sucesso."}
