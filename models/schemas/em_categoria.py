from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any
from .categorias import CategoriasResponse
from .produtos import ProdutosResponse

class ProdutoCategoriasResponse(ProdutosResponse):
    categorias: List[CategoriasResponse]
    
class CategoriaProdutosResponse(CategoriasResponse):
    produtos: List[ProdutosResponse]
    
class EmCategoriaCreate(BaseModel):
    id_categoria: int
    id_produto: int