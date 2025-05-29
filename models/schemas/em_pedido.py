from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any
from .pedidos import PedidosResponse
from .usuarios import UsuarioResponse

class EmPedidoBase(BaseModel):
    id_pedido: int = Field(description="Id do pedido")
    id_produto: int = Field(description="Id do produto")

class EmPedidoCreate(EmPedidoBase):
    pass

class EmPedidoResponse(BaseModel):
    id_em_pedido: int = Field(description="Id da relação entre o pedido e produto")

class EmPedidoPatch(EmPedidoCreate):
    pass

class PedidoFullResponse(BaseModel):
    usuario: UsuarioResponse
    produtos: List[PedidosResponse]
    