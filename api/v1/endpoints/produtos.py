from fastapi import APIRouter, Path, Query, HTTPException
from typing import List, Annotated
from models.db_models import ProdutosDB
from models.schemas import produtos
from main import db_dependency

router = APIRouter(prefix='/produtos', tags=['produtos'])

@router.get('/')
async def buscar_produto(
    db: db_dependency
) -> List[produtos.ProdutosResponse]|produtos.ProdutosResponse:
    db_produto = db.query(ProdutosDB)
    return db_produto

@router.post('/')
async def criar_produto(
    produto: produtos.ProdutosCreate, 
    db: db_dependency
):
    db_produto = ProdutosDB(**produto.model_dump())
    db.add(db_produto)
    db.commit()

@router.patch('/')
async def alterar_produto(
    id_prod: Annotated[int, Query(description="Id do produto")],
    produto: produtos.ProdutosPatch,
    db: db_dependency 
):
    print(produto.model_dump(exclude_defaults=True))
    #db.query(ProdutosDB).filter(ProdutosDB.id_prod == id_prod).update(produto.model_dump(exclude_defaults=True))
    #db.commit()
    return