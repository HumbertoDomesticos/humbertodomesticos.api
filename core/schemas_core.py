from fastapi import Depends
from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic

class QueryMeta(BaseModel):
    limit: int = Field(default=10, description="Limite de valores retornados")
    offset: int = Field(default=0, description="Quantidade de valores 'pulados'")
    
    @classmethod
    def as_query(cls):
        return Depends(cls)

class PaginationMeta(BaseModel):
    limit: int
    offset: int
    total: int
    
DataItem = TypeVar('DataItem')

class PaginatedResponse(BaseModel, Generic[DataItem]):
    data: List[DataItem]
    meta: PaginationMeta
    
def get_pagination_response(
    limit: int,
    offset: int,
    total: int,
    data: List[DataItem]
) -> PaginatedResponse:
    return PaginatedResponse(
        meta=PaginationMeta.model_validate(
            {
                "limit": limit, 
                "offset": offset, 
                "total": total
                }
            ), data=data)