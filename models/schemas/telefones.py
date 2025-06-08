from pydantic import Field, computed_field, BaseModel as Base
from typing import List, Optional

class TelefoneBase(Base):
    numero_telefone: Optional[str] = Field(default=None, description="Número do telefone", examples=["12345678901"], min_length=11, max_length=11)

class TelefoneId(Base):
    id_telefone: Optional[int] = Field(default=None, description="Id do telefone")

class TelefoneResponse(TelefoneBase):
    numero_telefone: Optional[str] = Field(default=None, exclude=True)

    @computed_field
    @property
    def telefone(self) -> str:
        return "({}) {}-{}".format(
            self.numero_telefone[:2],
            self.numero_telefone[2:7],
            self.numero_telefone[7:])
    
class TelefoneCreate(TelefoneBase):
    pass