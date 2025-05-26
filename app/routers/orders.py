from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, dependencies

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db)):
    return crud.order.create_order(db, order)

@router.get("/", response_model=list[schemas.OrderOut])
def list_orders(skip: int = 0, limit: int = 10, status: str = None, db: Session = Depends(dependencies.get_db)):
    return crud.order.get_orders(db, skip, limit, status)

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(dependencies.get_db)):
    order = crud.order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.put("/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(dependencies.get_db)):
    return crud.order.update_order(db, order_id, order)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.order.delete_order(db, order_id)
