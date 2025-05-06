from pydantic import BaseModel
from typing import Annotated, List, Any

class ProdutosBase(BaseModel):
    nome_prod: str
    preco_prod: float
    desconto_prod: int

class ProdutosResponse(ProdutosBase):
    id_prod: int

class ProdutosCreate(ProdutosBase):
    pass