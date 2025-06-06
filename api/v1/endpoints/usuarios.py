from fastapi import APIRouter, Path, Query, HTTPException
from pydantic import EmailStr
from passlib.context import CryptContext
from sqlalchemy import update
from typing import List, Annotated
from models.db_models import UsuariosDB, PedidosDB
from models.schemas import usuarios, pedidos
from main import db_dependency

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

@router.get('/', description="Busca por usuários")
async def get_usuarios(
    db: db_dependency
) -> List[usuarios.UsuarioResponse]|usuarios.UsuarioResponse:
    db_usuarios = db.query(UsuariosDB).all()
    return db_usuarios

@router.post('/', description="Insere um novo usuário ao banco de dados, endpoint relacionado com o registro de usuários")
async def insert_usuario(
    usuario: usuarios.UsuarioCreate,
    db: db_dependency
):
    db_usuario = UsuariosDB(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()

@router.patch('/', description="Altera os dados de um usuário") # TODO Implementar a alteração de usuário
async def update_usuario(
    db: db_dependency
):
    pass

@router.delete('/', description="Altera o 'estado' de um usuário (ativo ou inativo)")
async def delete_usuario(
    id_usuario: Annotated[str, Query(description="Usuário de Id")],
    db: db_dependency
):
    query = update(UsuariosDB).where(UsuariosDB.id_usuario == id_usuario).values(ativo_usuario = False)
    db.execute(query)
    db.commit()
    return 

@router.post('/admin', description="Transforma um usuário em um administrador")
async def set_admin_usuario(
    id_usuario: Annotated[int, Query(description="Id do usuário")],
    db: db_dependency
):
    query = update(UsuariosDB).where(UsuariosDB.id_usuario == id_usuario).values(admin_usuario = True)  
    db.execute(query)
    db.commit()
    return

@router.get('/auth', description="Busca se um usuário é um usuário")
async def auth_admin_usuario(
    email_usuario: Annotated[EmailStr, Query(description="Email do usuário")],
    db: db_dependency
):
    query = db.query(UsuariosDB).filter(UsuariosDB.email_usuario == email_usuario).first()
    if query.admin_usuario:
        return True
    else:
        return False

@router.post('/auth', description="Faz a autenticação para login do usuário no banco de dados")
async def auth_usuario(
    usuario: usuarios.UsuarioAuthLogin,
    db: db_dependency
):
    query = db.query(UsuariosDB).filter(UsuariosDB.email_usuario == usuario.email_usuario).first()
    if query.ativo_usuario:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(usuario.senha_usuario, query.senha_usuario)
    else:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_context.verify(usuario.senha_usuario, query.senha_usuario):
            return {"msg": "Senha está correta, mas a conta está inatíva"}
        else:
            return False
        
@router.get('/{id_usuario}/pedidos', description="Busca o pedido atual desse usuário. Caso não haja pedido aberto, cria um novo")
async def get_pedido_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    db: db_dependency
):
    stmt = db.get(UsuariosDB, id_usuario)
    ultimo_pedido = stmt.pedidos[-1]
    if ultimo_pedido.status_pedido:
        return ultimo_pedido
    else:
        db.add(PedidosDB(**pedidos.PedidosCreate(id_usuario_pedido=id_usuario).model_dump()))
        db.commit()
        return stmt.pedidos[-1]
        

@router.get('/{id_usuario}/pedidos/fechar', description="Fecha o último pedido criado")
async def close_pedido_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    db: db_dependency
):
    stmt = db.get(UsuariosDB, id_usuario)
    stmt.pedidos[-1].status_pedido = False
    db.commit()