
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_user, get_current_admin_user

router = APIRouter(
    prefix="/clients",
    tags=["Clientes"]
)


@router.post("/", response_model=schemas.Client, status_code=status.HTTP_201_CREATED,
             summary="Cria um novo cliente",
             description="Cria um novo registro de cliente, validando unicidade de e-mail e CPF. Requer privilégios de administrador.")
async def create_client(
    client: schemas.ClientCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Cria um novo cliente na base de dados.
    """
    db_client_email = crud.get_client_by_email(db, email=client.email)
    if db_client_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )
    db_client_cpf = crud.get_client_by_cpf(db, cpf=client.cpf)
    if db_client_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado."
        )
    return crud.create_client(db=db, client=client)

@router.get("/", response_model=List[schemas.Client],
            summary="Lista todos os clientes",
            description="Recupera uma lista de todos os clientes, com opções de paginação e filtragem por nome e e-mail. Requer autenticação.")
async def read_clients(
    skip: int = Query(0, ge=0, description="Número de registros para pular."),
    limit: int = Query(100, ge=1, le=200, description="Número máximo de registros a serem retornados."),
    name: Optional[str] = Query(None, description="Filtrar clientes pelo nome (parcial ou completo)."),
    email: Optional[str] = Query(None, description="Filtrar clientes pelo e-mail (parcial ou completo)."),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Lista todos os clientes com opções de paginação e filtro.
    """
    clients = crud.get_clients(db, skip=skip, limit=limit, name=name, email=email)
    return clients

@router.get("/{client_id}", response_model=schemas.Client,
            summary="Obtém informações de um cliente",
            description="Recupera os detalhes de um cliente específico pelo ID. Requer autenticação.")
async def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) 
):
    """
    Obtém um cliente pelo ID.
    """
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")
    return db_client


@router.put("/{client_id}", response_model=schemas.Client,
            summary="Atualiza um cliente existente",
            description="Atualiza as informações de um cliente existente pelo ID. Requer privilégios de administrador.")
async def update_client(
    client_id: int,
    client: schemas.ClientUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Atualiza um cliente existente.
    """

    db_client = crud.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")


    if client.email is not None and client.email != db_client.email:
        existing_client_email = crud.get_client_by_email(db, email=client.email)
        if existing_client_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Novo e-mail já cadastrado.")
    if client.cpf is not None and client.cpf != db_client.cpf:
        existing_client_cpf = crud.get_client_by_cpf(db, cpf=client.cpf)
        if existing_client_cpf:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Novo CPF já cadastrado.")


    update_data = client.model_dump(exclude_unset=True)
                                                      
    for key, value in update_data.items():
        setattr(db_client, key, value)

    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client



@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Exclui um cliente",
               description="Exclui um cliente específico pelo ID. Requer privilégios de administrador.")
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user) 
):
    """
    Deleta um cliente pelo ID.
    """
 
    deleted_count = crud.delete_client(db, client_id=client_id)
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")
    return