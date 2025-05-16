from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, List, Any

class ImagemBase(BaseModel):
    path_image: Annotated[str, Field(title="Caminho ou link até a imagem")]

class ImagemResponse(ImagemBase):
    id_image: Annotated[int, Field(title="ID da imagem")]
    id_prod_image: Annotated[int, Field(title="ID do produto que está na foto")] 

class ImagemCreate(ImagemBase):
    id_prod_image: Annotated[int, Field(title="ID do produto que está na foto")] 