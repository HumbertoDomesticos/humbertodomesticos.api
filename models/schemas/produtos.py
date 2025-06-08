from pydantic import Field, field_validator, computed_field, BaseModel as Base
from typing import List, Optional
from core import QueryMeta
from .categorias import CategoriaBase
from .imagens import ImagemURL

class ProdutoBase(Base):
    descritivo_produto: Optional[str] = Field(default="", description="Nome do produto", examples=["nome_produto"])
    descricao_produto: Optional[str] = Field(default="", description="Descrição do produto", examples=[""])
    preco_produto: Optional[float] = Field(default=None, description="Preço do produto")
    desconto_produto: Optional[int] = Field(default=None, description="Desconto do produto")
    estoque_produto: Optional[int] = Field(default=None, description="Estoque do produto")
    ativo_produto: Optional[bool] = Field(default=None, description="Produto está ativo ou não")

class ProdutoId(Base):
    id_produto: Optional[int] = Field(default=None, description="Id do produto")
    
class ProdutoResponse(ProdutoBase, ProdutoId):
    preco_produto: Optional[float] = Field(exclude=True)
    desconto_produto: Optional[int] = Field(exclude=True)
    imagens: Optional[List[ImagemURL]] = Field(description="Imagens do produto")
    categorias: Optional[List[CategoriaBase]] = Field(description="Categoria(s) do produto")

    def format_float_to_money_string(self, float_value: float):
        float_value_in_str = f"{float_value:.2f}"
        return f"R$ {float_value_in_str.replace('.', ',')}"

    @computed_field
    @property
    def preco(self) -> str:
        return self.format_float_to_money_string(float_value = (self.preco_produto))
    
    @computed_field
    @property
    def preco_descontado(self) -> str:
        return self.format_float_to_money_string(float_value = (self.preco_produto * (1 - self.desconto_produto/100)))
    
    @computed_field
    @property
    def desconto(self) -> str:
        if self.desconto_produto == 0:
            return "Nenhum desconto"
        else:
            return f"{self.desconto_produto}%"
    
class ProdutoQuery(QueryMeta, ProdutoBase, ProdutoId):
    pass

class ProdutoCreate(ProdutoBase):
    imagens: List[ImagemURL] = Field(description="Imagens do produto")

class ProdutoUpdate(ProdutoCreate):
    descritivo_produto: Optional[str] = Field(default=None, description="Nome do produto")