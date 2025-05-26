from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas

def get_client_by_email(db: Session, email: str):
    return db.query(models.Clients).filter(models.Clients.email == email).first()

def get_client_by_cpf(db: Session, cpf: str):
    return db.query(models.Clients).filter(models.Clients.cpf == cpf).first()

def create_client(db: Session, client: schemas.ClientCreate):
    if get_client_by_email(db, client.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado.")
    if get_client_by_cpf(db, client.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado.")
    
    db_client = models.Clients(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client(db: Session, client_id: int):
    return db.query(models.Clients).filter(models.Clients.id == client_id).first()

def update_client(db: Session, client_id: int, client: schemas.ClientCreate): 
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")
    
    for campo, valor in client.dict().items():
        setattr(db_client, campo, valor)

    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")
    
    db.delete(db_client)
    db.commit()
    return {"detail": "Cliente deletado com sucesso."}
