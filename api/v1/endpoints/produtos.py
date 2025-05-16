from fastapi import APIRouter, Path, Query, HTTPException
from sqlalchemy import text
from typing import List, Annotated
from models.db_models import ProdutosDB, em_categoria as cat_table
from models.schemas import produtos, em_categoria, categorias
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
    
    return

@router.post('/add-categoria')
async def insert_em_cat(
    em_cat: em_categoria.EmCategoriaCreate,
    db: db_dependency
):
    db.execute(text("INSERT INTO em_categoria (id_categoria, id_produto) VALUES (:id_categoria, :id_produto)"), {"id_categoria": em_cat.id_categoria, "id_produto": em_cat.id_produto})
    db.commit()
    
@router.get('/{id_prod}/categorias')
async def get_categorias_produto(
    id_prod: Annotated[int, Path(description="Id do produto")],
    db: db_dependency
) -> list[em_categoria.ProdutoCategoriasResponse]:
    query = db.query(ProdutosDB)
    return query