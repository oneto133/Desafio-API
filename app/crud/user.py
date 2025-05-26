from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
from app.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    hashed_pw = hash_password(user.senha)
    db_user = models.Users(
        username=user.username,
        email=user.email,
        senha=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()
