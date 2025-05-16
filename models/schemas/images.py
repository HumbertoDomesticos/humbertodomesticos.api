from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any
from .dependecies import convert_to_optional

class ImageBase(BaseModel):
    path_image: Annotated[str, Field(title="Caminho ou link até a imagem", default="string")]
    id_prod_image: Annotated[int, Field(title="ID do produto que está na foto", default=0)]

class ImageResponse(ImageBase):
    id_image: Annotated[int, Field(title="ID da imagem", default=0)]

class ImageCreate(ImageBase):
    pass

class ImagePatch(ImageCreate):
    __annotations__ = convert_to_optional(ImageCreate)