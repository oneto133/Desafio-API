from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, dependencies

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(dependencies.get_db)):
    return crud.product.create_product(db, product)

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 10, secao: str = None, db: Session = Depends(dependencies.get_db)):
    return crud.product.get_products(db, skip, limit, secao)

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(dependencies.get_db)):
    product = crud.product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(dependencies.get_db)):
    return crud.product.update_product(db, product_id, product)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.product.delete_product(db, product_id)
