from pydantic import BaseModel, Field
from typing import Annotated
from .dependecies import convert_to_optional

class TelefonesBase(BaseModel):
    numero_telefone: Annotated[str, Field(description="Número do telefone")]

class EnderecosResponse(TelefonesBase):
    id_telefone: Annotated[int, Field(description="Id do telefone")]

class EnderecosCreate(TelefonesBase):
    pass

class EnderecosPatch(TelefonesBase):
    __annotations__ = convert_to_optional(TelefonesBase)