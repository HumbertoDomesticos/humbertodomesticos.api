from pydantic import Field, computed_field, BaseModel as Base
from typing import List, Optional
import enum

class UnidadesFederativasEnum(enum.StrEnum):
    AC = enum.auto()
    AL = enum.auto()
    AP = enum.auto()
    AM = enum.auto()
    BA = enum.auto()
    CE = enum.auto()
    ES = enum.auto()
    GO = enum.auto()
    DF = enum.auto()
    MA = enum.auto()
    MT = enum.auto()
    MS = enum.auto()
    MG = enum.auto()
    PA = enum.auto()
    PB = enum.auto()
    PR = enum.auto()
    PE = enum.auto()
    PI = enum.auto()
    RJ = enum.auto()
    RN = enum.auto()
    RS = enum.auto()
    RO = enum.auto()
    RR = enum.auto()
    SC = enum.auto()
    SP = enum.auto()
    SE = enum.auto()
    TO = enum.auto()

class EnderecoBase(Base):
    cep_endereco: Optional[str] = Field(default=None, description="CEP do endereço do usuário", min_length=8, max_length=8, examples=["12345678"])
    numero_endereco: Optional[str] = Field(default=None, description="Número do endereço do usuário", examples=["1", "2", "50"])
    rua_endereco: Optional[str] = Field(default=None, description="Rua do endereço do usuário")
    bairro_endereco: Optional[str] = Field(default=None, description="Bairro do endereço do usuário")
    cidade_endereco: Optional[str] = Field(default=None, description="Cidade do endereço do usuário")
    descricao_endereco: Optional[str] = Field(default=None, description="Descrição do endereço do usuário")
    uf_endereco: Optional[UnidadesFederativasEnum] = Field(default=None, description="UF do endereço do usuário")

class EnderecoId(Base):
    id_endereco: Optional[int] = Field(default=None, description="Id do endereço")

class EnderecoResponse(EnderecoBase, EnderecoId):
    cep_endereco: Optional[str] = Field(default=None, exclude=True)

    @computed_field
    @property
    def cep(self) -> str:
        return "{}-{}".format(
            self.cep_endereco[0:5],
            self.cep_endereco[5:]
        )

    pass

class EnderecoCreate(EnderecoBase):
    pass