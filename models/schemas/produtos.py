from pydantic import BaseModel, Field, field_validator, computed_field
from decimal import Decimal
from typing import Annotated, List, Any, Optional
from .images import ImageCreate
from .dependecies import convert_to_optional

class ProdutosBase(BaseModel):
    nome_prod: Annotated[str, Field(description="Nome do produto", default='string')]
    descricao_prod: Annotated[str, Field(description="Descrição do produto", default='string')]
    preco_prod: Annotated[Decimal, Field(description="Preço do produto", ge=0, decimal_places=2, default=Decimal('0'))]
    desconto_prod: Annotated[int, Field(description="Desconto do produto", ge=0, le=100, default=0)]
    estoque_prod: Annotated[int, Field(ge=0)]

class ProdutosResponse(ProdutosBase):
    id_prod: Annotated[int, Field(description="Id do produto")]
    preco_prod: Annotated[float, Field(description="Preço do produto", exclude=True)]
    estoque_prod: Annotated[int, Field(title="Estoque do produto", ge=0)]
    
    @computed_field
    @property
    def preco_produto(self) -> Annotated[str, Field(description="Preço do produto formatado")]:
        return f"R${"%.2f" % self.preco_prod}".replace('.', ',')
    
    @computed_field
    @property
    def desconto_preco_produto(self) -> Annotated[str, Field(description="Preço do produto com desconto e formatado")]:
        return f"R${"%.2f" % (self.preco_prod * (1 - (self.desconto_prod / 100)))}".replace('.', ',')

class ProdutosCreate(ProdutosBase):
    images_prod: Annotated[List[ImageCreate], Field(description="Images do produto", min_length=1, max_length=4, default_factory=list)]
    # TODO Valor padrão NÃO tá funcionando, caso ele receba um valor padrão ele deve ignorar o valor e não mostrar nada

class ProdutosPatch(ProdutosBase):
    __annotations__ = convert_to_optional(ProdutosBase)
    images_prod: Annotated[Optional[List[ImageCreate]], Field(description="Images do produto", min_length=1, max_length=4, default_factory=list)]