from pydantic import BaseModel, Field, field_validator, EmailStr, computed_field
from passlib.context import CryptContext
from typing import Annotated, List, Any
from datetime import date
from .dependecies import convert_to_optional

class UsuarioBase(BaseModel):
    nome_usuario: Annotated[str, Field(description="Nome que será mostrado no perfil do usuário")]
    email_usuario: Annotated[EmailStr, Field(description="Email do usuário")]
    data_nasc_usuario: Annotated[date, Field(description="Data de nascimento do usuário")]

class UsuarioResponse(UsuarioBase):
    pass

class UsuarioCreate(UsuarioBase):
    senha_usuario_temp: Annotated[str, Field(description="Senha do usuário", exclude=True)]
    
    @computed_field
    @property
    def senha_usuario(self) -> Annotated[str, Field(description="Senha do usuário em hash BCRYPT")]:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(self.senha_usuario_temp) # TODO Senha deve ser hasheada antes de ser enviada ao banco

class UsuarioPatch(UsuarioCreate):
    __annotations__ = convert_to_optional(UsuarioCreate)