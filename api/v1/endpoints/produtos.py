from fastapi import APIRouter, Query, Path
from database import DbSessionDep, Session
from typing import Dict, Tuple, List, Union, Annotated, Set

from core import apply_filters_from_model, get_pagination_response, PaginatedResponse, DEFAULT_NON_FILTER_FIELDS
from models.schemas import produtos, imagens
from models.db_models import ProdutosDB, EmCategoriaDB, ImagensDB

router = APIRouter(prefix="/produtos", tags=["Produtos"])

PRODUTOS_FILTER_CONFIG: Dict[str, Tuple[str, str]] = {
    "id_produto": ("id_produto", "eq"),
    "descritivo_produto": ("descritivo_produto", "contains"),
    "descricao_produto": ("descricao_produto", "contains"),
    "desconto_produto": ("desconto_produto", "eq"),
    "ativo_produto": ("ativo_produto", "eq")
}

PRODUTOS_NON_FILTER_FIELDS: Set[str] = {"limit", "offset", "sort_by", "order_by", "preco_produto", "estoque_produto", "imagens", "categorias"}

@router.get('/', 
            response_model=PaginatedResponse[produtos.ProdutoResponse],
            description="Busca os produtos")
def get_produtos(
    query: produtos.ProdutoQuery = produtos.ProdutoQuery.as_query(),
    db: Session = DbSessionDep
):
    stmt = db.query(ProdutosDB)
    stmt = apply_filters_from_model(
        stmt,
        ProdutosDB,
        query,
        PRODUTOS_FILTER_CONFIG,
        PRODUTOS_NON_FILTER_FIELDS
    )
    total = stmt.count()
    resp_value = stmt.order_by(ProdutosDB.id_produto.asc()).offset(query.offset).limit(query.limit).all()
    return get_pagination_response(query.limit, query.offset, total, resp_value)

@router.post('/',
             response_model=produtos.ProdutoResponse,
             description="Cria um novo produto")
def post_produtos(
    body: produtos.ProdutoCreate,
    db: Session = DbSessionDep
):
    db.add(ProdutosDB(**body.model_dump()))
    db.commit()
    return db.query(ProdutosDB).order_by(ProdutosDB.id_produto.desc()).limit(1).first()

@router.patch('/', 
              response_model=produtos.ProdutoResponse,
              description="Altera os dados de um produto")
def patch_produtos(
    id_produto: Annotated[int, Query(description="ID do produto que será alterado")],
    body: produtos.ProdutoUpdate,
    db: Session = DbSessionDep
):
    dump_class = body.model_dump(exclude_unset=True)
    stmt = db.get(ProdutosDB, id_produto)
    for k, val in dump_class.items():
        if hasattr(stmt, k):
            setattr(stmt, k, val)
    db.commit()    
    
@router.post('/{id_produto}/add-imagem',
             response_model=produtos.ProdutoResponse,
             description="Adiciona uma imagem ao produto")
def add_imagem_produto(
    id_produto: Annotated[int, Path(description="Id do produto")],
    body: imagens.ImagemURL,
    db: Session = DbSessionDep
):
    stmt = db.get(ProdutosDB, id_produto)
    if stmt is None:
        return False
    print(body.model_dump())
    stmt.imagens.append(ImagensDB(id_produto_fk = id_produto, **body.model_dump()))
    db.commit()
    db.refresh(stmt)
    return stmt

@router.delete('/',
               response_model=str,
               description="Deleta um produto")
def delete_produtos(
    id_produto: Annotated[int, Query(description="ID do produtos que será deletado")],
    db: Session = DbSessionDep
):
    stmt = db.get(ProdutosDB, id_produto)
    db.delete(stmt)
    db.commit()
    return f"Produto com id: {id_produto}"

@router.post('/{id_produto}/{id_categoria}',
             response_model=produtos.ProdutoResponse,
             description="Adiciona uma categoria a um produto")
def add_categoria_produto(
    id_produto: Annotated[int, Path(description="ID do produto")],
    id_categoria: Annotated[int, Path(description="ID da categoria")],
    db: Session = DbSessionDep
):
    stmt = EmCategoriaDB(id_prod_fk = id_produto, id_categoria_fk = id_categoria)
    db.add(stmt)
    db.commit()
    return db.get(ProdutosDB, id_produto)