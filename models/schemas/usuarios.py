from pydantic import Field, computed_field, EmailStr, SecretStr, BaseModel as Base
from typing import List, Optional
from core import QueryMeta, get_password_hash
from .telefones import TelefoneResponse
from .enderecos import EnderecoResponse
import enum

class GeneroEnum(enum.StrEnum):
    MASCULINO = enum.auto()
    FEMININO = enum.auto()
    OUTRO = enum.auto()

class UsuarioBase(Base):
    nome_usuario: Optional[str] = Field(default=None, description="Nome do usuário", examples=["nome_usuario"])
    email_usuario: Optional[EmailStr] = Field(default=None, description="Email do usuário")
    genero_usuario: Optional[GeneroEnum] = Field(default=None, description="Gênero do usuário")
    cpf_usuario: Optional[str] = Field(default=None, description="CPF do usuário", examples=["12345678901"], min_length=11, max_length=11)

class UsuarioId(Base):
    id_usuario: Optional[int] = Field(default=None, description="Id do usuário")

class UsuarioResponse(UsuarioBase, UsuarioId):
    telefones: Optional[List[TelefoneResponse]] = Field(default=None, description="Telefones do usuário")
    enderecos: Optional[List[EnderecoResponse]] = Field(default=None, description="Endereços do usuário")
    
    cpf_usuario: Optional[str] = Field(exclude=True)

    @computed_field
    @property
    def cpf(self) -> Optional[str]:
        if self.cpf_usuario is None:
            return None
        else:
            return "{}.{}.{}-{}".format(
                self.cpf_usuario[:3],
                self.cpf_usuario[3:6],
                self.cpf_usuario[6:9],
                self.cpf_usuario[9:]
            )

class UsuarioQuery(QueryMeta, UsuarioBase, UsuarioId):
    pass

class UsuarioCreate(UsuarioBase):
    senha_usuario_temp: Optional[str] = Field(default=None, description="Senha do usuário em plain text", exclude=True)

    @computed_field
    @property
    def senha_usuario(self) -> str:
        return get_password_hash(self.senha_usuario_temp)

class UsuarioUpdate(UsuarioCreate):
    descritivo_usuario: Optional[str] = Field(default=None, description="Nome da Usuario")

class UsuarioVerify(Base):
    email_usuario: EmailStr = Field(description="Email do usuário")
    senha_usuario: str = Field(description="Senha do usuário em plain text")