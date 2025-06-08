from pydantic import Field, BaseModel as Base
from typing import List, Optional
from core import QueryMeta
from .categorias import CategoriaResponse
from .produtos import ProdutoResponse

class ProdutosEmCategoria(Base):
    categoria: CategoriaResponse
    produtos: List[ProdutoResponse]