from fastapi import APIRouter, Path, Query, HTTPException
from typing import List, Annotated
from models.db_models import EnderecosDB
from models.schemas import enderecos
from main import db_dependency

router = APIRouter(prefix='/enderecos', tags=['enderecos'])

@router.get('/')
async def get_enderecos(
    db: db_dependency
):
    query = db.query(EnderecosDB)
    return query