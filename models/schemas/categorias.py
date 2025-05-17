from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any

class CategoriasBase(BaseModel):
    descritivo_categoria: Annotated[str, Field(description="Nome da categoria")]

class CategoriasResponse(CategoriasBase):
    id_categoria: Annotated[int, Field(description="ID da categoria")]

class CategoriasCreate(CategoriasBase):
    pass