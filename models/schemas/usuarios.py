from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Annotated, List, Any
from datetime import date
from .dependecies import convert_to_option

class UsuarioBase(BaseModel):
    nome_usuario: Annotated[str, Field(description="Nome que será mostrado no perfil do usuário")]
    email_usuario: Annotated[EmailStr, Field(description="Email do usuário")]

class UsuarioResponse(UsuarioBase):
    data_nasc_usuario: Annotated[date, Field(description="Data de nascimento do usuário")]

class UsuarioRegister(UsuarioBase):
    senha_usuario: Annotated[str, Field(description="Senha do usuário")]
    senha_hash_usuario: Annotated[str, Field(description="Senha do usuário em hash BCRYPT")]

class UsuarioPatch(UsuarioRegister):
    __annotations__ = convert_to_option(UsuarioRegister)