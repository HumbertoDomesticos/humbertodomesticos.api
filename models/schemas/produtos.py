from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from typing import Annotated, List, Any, Optional
from .images import ImageCreate
from .dependecies import convert_to_optional

class ProdutosBase(BaseModel):
    nome_prod: Annotated[str, Field(title="Nome do produto", default='string')]
    preco_prod: Annotated[Decimal, Field(title="Preço do produto", ge=0, decimal_places=2, default=Decimal('0'))]
    desconto_prod: Annotated[int, Field(title="Desconto do produto", ge=0, le=100, default=0)]

class ProdutosResponse(ProdutosBase):
    id_prod: int

class ProdutosCreate(ProdutosBase):
    images_prod: Annotated[List[ImageCreate], Field(title="Images do produto", min_length=1, max_length=4, default_factory=list)]
    # TODO Valor padrão NÃO tá funcionando, caso ele receba um valor padrão ele deve ignorar o valor e não mostrar nada

class ProdutosPatch(ProdutosBase):
    __annotations__ = convert_to_optional(ProdutosBase)
    images_prod: Annotated[Optional[List[ImageCreate]], Field(title="Images do produto", min_length=1, max_length=4, default_factory=list)]