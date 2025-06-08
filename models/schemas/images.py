from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any
from .dependecies import convert_to_optional

class ImageBase(BaseModel):
    path_image: Annotated[str, Field(description="Caminho ou link até a imagem", default="string")]

class ImageResponse(ImageBase):
    id_image: Annotated[int, Field(description="ID da imagem", default=0)]

class ImageCreate(ImageBase):
    pass

class ImagePatch(ImageCreate):
    __annotations__ = convert_to_optional(ImageCreate)