from fastapi import APIRouter, Path, Query, HTTPException
from typing import List, Annotated
from models.db_models import UsuariosDB
from models.schemas import usuarios
from main import db_dependency

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

@router.get('/')
async def get_usuarios(
    db: db_dependency
) -> List[usuarios.UsuarioResponse]|usuarios.UsuarioResponse:
    db_usuarios = db.query(UsuariosDB).all()
    return db_usuarios

@router.post('/')
async def insert_usuario(
    usuario: usuarios.UsuarioCreate,
    db: db_dependency
):
    db_usuario = UsuariosDB(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
