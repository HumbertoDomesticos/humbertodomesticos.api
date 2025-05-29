from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Annotated, List, Any, Optional
from datetime import date
from .produtos import ProdutosResponse
from .response import PaginacaoBase, QueryBase

class PedidosBase(BaseModel):
    id_usuario_pedido: Optional[int] = Field(default=None, description="Id do usuário que fez o pedido")
    status_pedido: Optional[bool] = Field(default=True, description="Estado do pedido")
    data_ultima_mudanca_pedido: Optional[date] = Field(default=date.today() ,description="Data da última mudança")

class PedidosCreate(PedidosBase):
    pass

class PedidosResponse(PedidosBase):
    pass

class PedidosPatch(PedidosCreate):
    pass

class PedidosListingResponse(BaseModel):
    pedidos: List[PedidosResponse]
    paginacao: PaginacaoBase
    
class PedidoQuery(QueryBase, PedidosCreate):
    pass