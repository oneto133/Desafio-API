
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db
from .routers import auth, clients, products, orders
from .config import settings

app = FastAPI(
    title="Lu Estilo API",
    description="API RESTful para gerenciar clientes, produtos e pedidos da Lu Estilo.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.on_event("startup")
async def startup_event():

    print("Database tables ensured or migrations managed by Alembic.")


@app.get("/", summary="Verifica o status da API", description="Retorna uma mensagem de boas-vindas para verificar se a API está funcionando.")
async def root():
    return {"message": "API Lu Estilo está funcionando! Acesse /docs para a documentação Swagger."}