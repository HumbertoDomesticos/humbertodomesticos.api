from fastapi import APIRouter, Path, Query, HTTPException
from sqlalchemy import text, select, and_
from typing import List, Annotated
from models.db_models import PedidosDB, EmPedidoDB
from models.schemas import pedidos, em_pedido
from main import db_dependency

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get('/')
async def get_pedidos(
    pedido_query: pedidos.PedidoQuery = pedidos.PedidoQuery.as_query(),
    db: db_dependency = None
) -> pedidos.PedidosListingResponse: 
    filters = pedido_query.model_dump(exclude_defaults=True, exclude_none=True)

    conditions = []
    for field, value in filters.items():
        if hasattr(PedidosDB, field):
            conditions.append(getattr(PedidosDB, field) == value)
    
    query = db.query(PedidosDB).where(and_(*conditions)).offset(pedido_query.offset).limit(pedido_query.limit)
    return_value = db.execute(query).mappings().all()
    
    return {'pedidos': return_value, 'paginacao': {'limit': pedido_query.limit, 'offset': pedido_query.offset, 'total': query.count()}}

@router.post('/')
async def post_pedidos(
    pedidos: pedidos.PedidosCreate,
    db: db_dependency
):
    pedido_db = PedidosDB(**pedidos.model_dump())
    db.add(pedido_db)
    db.commit()
    return

@router.get('/{id_pedido}/produtos')
async def get_produtos_pedido(
    id_pedido: Annotated[int, Path(description="Id do pedido")],
    db: db_dependency 
):
    stmt = db.get(PedidosDB, id_pedido)
    return stmt.produtos

@router.post('/produtos/inserir')
async def post_produto_pedido(
    id_usuario: int,
    id_produto: int,
    db: db_dependency
):
    stmt = db.query(PedidosDB).filter(PedidosDB.id_usuario_pedido == id_usuario)
    id_pedido = db.execute(stmt).mappings().all()[-1]["PedidosDB"].id_pedido
    
    db.add(EmPedidoDB(**em_pedido.EmPedidoCreate(id_pedido=id_pedido, id_produto=id_produto).model_dump()))
    db.commit()