from fastapi import APIRouter, Query, Path
from database import DbSessionDep, Session
from typing import Dict, Tuple, List, Union, Annotated

from core import apply_filters_from_model, get_pagination_response, PaginatedResponse, DEFAULT_NON_FILTER_FIELDS
from models.schemas import categorias
from models.db_models import CategoriasDB

router = APIRouter(prefix="/categorias", tags=["Categorias"])

CATEGORIAS_FILTER_CONFIG: Dict[str, Tuple[str, str]] = {
    "id_categoria": ("id_categoria", "eq"),
    "descritivo_categoria": ("descritivo_categoria", "contains")
}

@router.get('/', 
            response_model=PaginatedResponse[categorias.CategoriaResponse],
            description="Busca as categorias")
def get_categorias(
    query: categorias.CategoriaQuery = categorias.CategoriaQuery.as_query(),
    db: Session = DbSessionDep
):
    stmt = db.query(CategoriasDB)
    stmt = apply_filters_from_model(
        stmt,
        CategoriasDB,
        query,
        CATEGORIAS_FILTER_CONFIG,
        DEFAULT_NON_FILTER_FIELDS
    )
    total = stmt.count()
    resp_value = stmt.order_by(CategoriasDB.id_categoria.asc()).offset(query.offset).limit(query.limit).all()
    return get_pagination_response(query.limit, query.offset, total, resp_value)

@router.post('/', 
             response_model=categorias.CategoriaResponse, 
             description="Cria uma nova categoria")
def post_categorias(
    body: Union[List[categorias.CategoriaCreate], categorias.CategoriaCreate],
    db: Session = DbSessionDep
):
    if isinstance(body, list):
        for categoria in body:
            db.add(CategoriasDB(**categoria.model_dump()))
    else:
        db.add(CategoriasDB(**body.model_dump()))
    db.commit()
    stmt = db.query(CategoriasDB).order_by(CategoriasDB.id_categoria.desc()).limit(1)
    return stmt.first()

@router.patch('/', 
              response_model=categorias.CategoriaResponse,
              description="Altera os dados de uma categoria")
def patch_categorias(
    id_categoria: Annotated[int, Query(description="ID da categoria que será alterada")],
    body: categorias.CategoriaUpdate,
    db: Session = DbSessionDep
):
    dump_class = body.model_dump(exclude_unset=True)
    stmt = db.get(CategoriasDB, id_categoria)
    for k, val in dump_class.items():
        if hasattr(stmt, k):
            setattr(stmt, k, val)
    db.commit()    
    db.refresh(stmt)
    return stmt

@router.delete('/',
               response_model=str,
               description="Deleta uma categoria")
def delete_categorias(
    id_categoria: Annotated[int, Query(description="ID da categoria que será deletada")],
    db: Session = DbSessionDep
):
    stmt = db.get(CategoriasDB, id_categoria)
    db.delete(stmt)
    db.commit()
    return f"Categoria com id: {id_categoria} foi removido"