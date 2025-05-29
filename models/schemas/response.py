from fastapi import Depends
from pydantic import BaseModel, Field
from typing import List, Optional

class PaginacaoBase(BaseModel):
    limit: int = Field(default=10, gt=1, le=100)
    offset: int = Field(default=0)
    total: int = Field(default=0)
    
class QueryBase(BaseModel):
    limit: Optional[int] = Field(default=10)
    offset: Optional[int] = Field(default=0)
    
    @classmethod
    def as_query(cls):
        return Depends(cls)