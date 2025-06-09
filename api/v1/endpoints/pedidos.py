from fastapi import APIRouter, Query, Path
from database import DbSessionDep, Session
from typing import Dict, Tuple, List, Union, Annotated, Set
from datetime import datetime

from core import apply_filters_from_model, get_pagination_response, PaginatedResponse, DEFAULT_NON_FILTER_FIELDS
from models.schemas import pedidos, usuarios
from models.db_models import PedidosDB, EmPedidoDB, UsuariosDB

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

PEDIDOS_FILTER_CONFIG: Dict[str, Tuple[str, str]] = {
    "id_pedido": ("id_pedido", "eq"),
    "data_criacao_pedido": ("data_criacao_pedido", "contains"),
    "data_ultima_alteracao_pedido": ("data_ultima_alteracao_pedido", "contains"),
    "data_finalizacao_pedido": ("data_finalizacao_pedido", "eq"),
    "tipo_pagamento": ("tipo_pagamento", "eq"),
    "status_pedido": ("status_pedido", "eq")
}

PEDIDOS_NON_FILTER_FIELDS: Set[str] = {"limit", "offset", "sort_by", "order_by"}

@router.get('/{id_usuario}', 
            response_model=List[pedidos.PedidoResponse]|bool,
            description="Busca todos os pedidos do usuario")
def get_pedidos_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if stmt is not None:
        return stmt.pedidos
    else:
        return False
        

@router.post('/{id_usuario}',
             response_model=pedidos.PedidoResponse,
             description="Cria um pedido para o usuário")
def create_pedido_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    db: Session = DbSessionDep
):
    stmt = PedidosDB(id_usuario_fk = id_usuario)
    db.add(stmt)
    db.commit()

@router.get('/{id_usuario}/pedido-aberto', 
            response_model=pedidos.PedidoResponse|bool,
            description="Retorna o último pedido aberto do usuário, caso não haja, ele é criado") 
def get_pedido_aberto(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if stmt is None:
        return False
    if len(stmt.pedidos) != 0 and stmt.pedidos[-1].status_pedido == pedidos.StatusPedidoEnum.EM_CARRINHO:
        return stmt.pedidos[-1]
    else:
        create_pedido_usuario(id_usuario, db)
        db.refresh(stmt)
        return stmt.pedidos[-1]
    
@router.post('/{id_usuario}/add-produto/{id_produto}/{quantidade}', 
             response_model=pedidos.PedidoResponse|bool,
             description="Adiciona um produto ao pedido aberto do usuário")
def add_produto_em_pedido(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    id_produto: Annotated[int, Path(description="Id do produto")],
    quantidade: Annotated[int, Path(description="Quantidade do produto")],
    db: Session = DbSessionDep
):
    pedido = get_pedido_aberto(id_usuario, db)
    if not pedido:
        return False
    if len(pedido.produtos_em_pedido) == 0 or next((produto for produto in pedido.produtos_em_pedido if produto.id_produto_fk == id_produto), None) is None:
        stmt = EmPedidoDB(id_pedido_fk = pedido.id_pedido, id_produto_fk = id_produto, quant_produto_em_pedido = quantidade)
        db.add(stmt)
    else:
        for produto in pedido.produtos_em_pedido:
            if produto.id_produto_fk == id_produto:
                produto.quant_produto_em_pedido += quantidade
                break   
    pedido.data_ultima_alteracao_pedido = datetime.now()
    db.commit()
    db.refresh(pedido)
    return pedido

@router.post('/{id_usuario}/alt-quant/{id_produto}/{quantidade}',
             response_model=pedidos.PedidoResponse|bool,
             description="Altera a quantidade de um produto ou o remove do pedido do usuário")
def alter_quant_produto_em_pedido(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    id_produto: Annotated[int, Path(description="Id do produto")],
    quantidade: Annotated[int, Path(description="Quantidade do produto")],
    db: Session = DbSessionDep
):
    pedido = get_pedido_aberto(id_usuario, db)
    if not pedido:
        return False
    for produto in pedido.produtos_em_pedido:
        if produto.id_produto_fk == id_produto and produto.quant_produto_em_pedido != quantidade and quantidade > 0:
            produto.quant_produto_em_pedido = quantidade
            pedido.data_ultima_alteracao_pedido = datetime.now()
            db.commit()
            db.refresh(pedido)
            return pedido
        elif produto.id_produto_fk == id_produto and quantidade == 0:
            db.delete(produto)
            pedido.data_ultima_alteracao_pedido = datetime.now()
            db.commit()
            db.refresh(pedido)
            return pedido
        else:
            return False
    
    
@router.post('/{id_usuario}/fechar-pedido', 
             response_model=pedidos.ProdutoResponse|bool,
             description="Passa o pedido para 'processando_pagamento'") 
def close_pedido_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    tipo_pagamento: pedidos.TiposPagamentoEnum = pedidos.TiposPagamentoEnum.NENHUM,
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if not stmt:
        return False
    if len(stmt.pedidos) != 0 and stmt.pedidos[-1].status_pedido == pedidos.StatusPedidoEnum.EM_CARRINHO:
        pedido_obj = stmt.pedidos[-1]
        pedido_obj.status_pedido = pedidos.StatusPedidoEnum.PROCESSANDO_PAGAMENTO
        pedido_obj.data_finalizacao_pedido = datetime.now()
        pedido_obj.tipo_pagamento = tipo_pagamento
        if pedido_obj.tipo_pagamento == pedidos.TiposPagamentoEnum.NENHUM:
            return False # Usuário deve selecionar algum tipo de pagamento
        db.commit()
        db.refresh(pedido_obj)
        return pedido_obj
    else:
        return False
    
@router.post('/{id_usuario}/alterar-pedido', 
             response_model=pedidos.ProdutoResponse|bool,
             description="Altera tipo de pagamento e status no pedido")
def update_pedido_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    tipo_pagamento: pedidos.TiposPagamentoEnum = pedidos.TiposPagamentoEnum.NENHUM,
    status_pedido: pedidos.StatusPedidoEnum = pedidos.StatusPedidoEnum.EM_CARRINHO,
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if stmt is None:
        return False
    if len(stmt.pedidos) != 0 and stmt.pedidos[-1].status_pedido == pedidos.StatusPedidoEnum.EM_CARRINHO:
        pedido_obj = stmt.pedidos[-1]
        pedido_obj.tipo_pagamento = tipo_pagamento if tipo_pagamento != pedidos.TiposPagamentoEnum.NENHUM else pedido_obj.tipo_pagamento
        pedido_obj.status_pedido = status_pedido if status_pedido != pedidos.StatusPedidoEnum.EM_CARRINHO else pedido_obj.status_pedido
        pedido_obj.data_ultima_alteracao_pedido = datetime.now()
        db.commit()
        db.refresh(pedido_obj)
        return pedido_obj
    else:
        return False