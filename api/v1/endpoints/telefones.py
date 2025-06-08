from fastapi import APIRouter, Path, Query, HTTPException
from typing import List, Annotated
from models.db_models import TelefonesDB
from models.schemas import telefones
from main import db_dependency

router = APIRouter(prefix='/telefones', tags=['telefones'])

@router.get('/')
async def get_telefones(
    db: db_dependency
):
    query = db.query(TelefonesDB)
    return query