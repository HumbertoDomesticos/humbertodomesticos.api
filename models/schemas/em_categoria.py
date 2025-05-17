from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any
from .categorias import CategoriasResponse
from .produtos import ProdutosResponse

class ProdutoCategoriasResponse(ProdutosResponse):
    categorias: Annotated[List[CategoriasResponse], Field(description="Categorias de um produto")]
    
class CategoriaProdutosResponse(CategoriasResponse):
    produtos: Annotated[List[ProdutosResponse], Field(description="Produtos dentro de uma categoria")]
    
class EmCategoriaCreate(BaseModel):
    id_categoria: Annotated[int, Field(description="Id da categoria")]
    id_produto: Annotated[int, Field(description="Id do produto")]