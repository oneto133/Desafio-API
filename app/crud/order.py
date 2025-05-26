from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Orders(
        numero_pedido=order.numero_pedido,
        data_pedido=order.data_pedido,
        status=order.status,
        valor_total=order.valor_total
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.itens:
        db_item = models.OrderItems(
            order_id=db_order.id,
            product_id=item.product_id,
            quantidade=item.quantidade,
            preco_unitario_no_pedido=item.preco_unitario_no_pedido
        )
        db.add(db_item)

    db.commit()
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Orders).filter(models.Orders.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10, status: str = None):
    query = db.query(models.Orders)
    if status:
        query = query.filter(models.Orders.status == status)
    return query.offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    for field, value in order.dict(exclude={"itens"}).items():
        setattr(db_order, field, value)

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(db_order)
    db.commit()
    return {"detail": "Pedido deletado com sucesso."}
