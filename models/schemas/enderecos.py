from pydantic import BaseModel, Field
from typing import Annotated
from .dependecies import convert_to_optional

class EnderecosBase(BaseModel):
    rua_endereco: Annotated[str, Field(description="Rua do endereço")]
    numero_endereco: Annotated[str, Field(description="Número do endereço")]
    bairro_endereco: Annotated[str, Field(description="Bairro do endereço")]
    cidade_endereco: Annotated[str, Field(description="Cidade do endereço")]
    uf_endereco: Annotated[str, Field(description="Unidade federal do endereço")]

class EnderecosResponse(EnderecosBase):
    pass

class EnderecosCreate(EnderecosBase):
    pass

class EnderecosPatch(EnderecosCreate):
    __annotations__ = convert_to_optional(EnderecosCreate)