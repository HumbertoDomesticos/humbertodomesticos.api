from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any
from .images import ImageCreate

class ProdutosBase(BaseModel):
    nome_prod: Annotated[str, Field(title="Nome do produto")]
    preco_prod: Annotated[Decimal, Field(title="Preço do produto", gt=0, decimal_places=2)]
    desconto_prod: Annotated[int, Field(title="Desconto do produto", ge=0, le=100)]

class ProdutosResponse(ProdutosBase):
    id_prod: int

class ProdutosCreate(ProdutosBase):
    images_prod: Annotated[List[ImageCreate], Field(title="Images do produto")]