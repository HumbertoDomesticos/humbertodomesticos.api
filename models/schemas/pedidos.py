from pydantic import Field, BaseModel as Base
from typing import List, Optional
import enum
from datetime import datetime
from .produtos import ProdutoResponse
from core import QueryMeta

class TiposPagamentoEnum(enum.StrEnum):
    PIX = enum.auto()
    TRANSF_BANC = enum.auto()
    NENHUM = enum.auto()

class StatusPedidoEnum(enum.StrEnum):
    EM_CARRINHO = enum.auto()
    PROCESSANDO_PAGAMENTO = enum.auto()
    PROCESSANDO_PEDIDO = enum.auto()
    A_CAMINHO = enum.auto()
    ENTREGUE = enum.auto()

class PedidoBase(Base):
    data_criacao_pedido: Optional[datetime] = Field(default=datetime.now(), description="Data de criação do pedido")
    data_ultima_alteracao_pedido: Optional[datetime] = Field(default=datetime.now(), description="Data da última alteração do pedido")
    data_finalizacao_pedido: Optional[datetime] = Field(default=None, description="Data de finalização do pedido")
    tipo_pagamento: Optional[TiposPagamentoEnum] = Field(default=TiposPagamentoEnum.NENHUM, description="Tipo de pagamento selecionado")
    status_pedido: Optional[StatusPedidoEnum] = Field(default=StatusPedidoEnum.EM_CARRINHO)

class PedidoId(Base):
    id_pedido: Optional[int] = Field(default=None, description="Id do pedido")

class PedidoResponse(PedidoBase, PedidoId):
    produtos_em_pedido: List["ProdutoEmPedidoResponse"]

class ProdutoEmPedidoResponse(Base):
    quant_produto_em_pedido: int
    produto: ProdutoResponse

class PedidoQuery(QueryMeta, PedidoBase, PedidoId):
    pass

class PedidoCreate(PedidoBase):
    pass