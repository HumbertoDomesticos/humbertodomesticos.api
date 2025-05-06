from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any

class ImageBase(BaseModel):
    path_image: Annotated[str, Field(title="Caminho ou link até a imagem")]

class ImageResponse(ImageBase):
    id_image: Annotated[int, Field(title="ID da imagem")]
    id_prod_image: Annotated[int, Field(title="ID do produto que está na foto")] 

class ImageCreate(ImageBase):
    id_prod_image: Annotated[int, Field(title="ID do produto que está na foto")] 