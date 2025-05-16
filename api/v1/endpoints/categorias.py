from fastapi import APIRouter, Path, Query, HTTPException
from typing import List, Annotated
from models.db_models import CategoriasDB
from models.schemas import categorias, em_categoria
from main import db_dependency

router = APIRouter(prefix='/categorias', tags=['categorias'])

@router.get('/')
async def get_categorias(
    db: db_dependency
) -> List[em_categoria.CategoriaProdutosResponse]|em_categoria.CategoriaProdutosResponse:
    db_categorias = db.query(CategoriasDB)
    return db_categorias

@router.post('/')
async def insert_categoria(
    categoria: categorias.CategoriasCreate,
    db: db_dependency
):
    db_categoria = CategoriasDB(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    
@router.get('/produtos')
async def get_produtos_categoria(
    db: db_dependency
) -> list[em_categoria.CategoriaProdutosResponse]:
    query = db.query(CategoriasDB)
    return query