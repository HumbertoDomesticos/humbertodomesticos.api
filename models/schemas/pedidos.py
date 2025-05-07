from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Annotated, List, Any
from datetime import date
from .produtos import ProdutosResponse

class PedidosBase(BaseModel):
    pass