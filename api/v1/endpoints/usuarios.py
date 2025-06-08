from fastapi import APIRouter, Query, Path
from database import DbSessionDep, Session
from typing import Dict, Tuple, List, Union, Annotated, Set

from core import apply_filters_from_model, get_pagination_response, PaginatedResponse, DEFAULT_NON_FILTER_FIELDS, verify_hash
from models.schemas import usuarios, telefones, enderecos, pedidos
from models.db_models import UsuariosDB, TelefonesDB, EnderecosDB, PedidosDB

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

USUARIOS_FILTER_CONFIG: Dict[str, Tuple[str, str]] = {
    "id_usuario": ("id_usuario", "eq"),
    "nome_usuario": ("nome_usuario", "contains"),
    "genero_usuario": ("genero_usuario", "eq"),
    "cpf_usuario": ("cpf_usuario", "eq")
}

USUARIOS_NON_FILTER_FIELDS: Set[str] = {"limit", "offset", "sort_by", "order_by", "telefones", "enderecos"}

@router.get('/', response_model=PaginatedResponse[usuarios.UsuarioResponse])
def get_usuarios(
    query: usuarios.UsuarioQuery = usuarios.UsuarioQuery.as_query(),
    db: Session = DbSessionDep
):
    stmt = db.query(UsuariosDB)
    stmt = apply_filters_from_model(
        stmt,
        UsuariosDB,
        query,
        USUARIOS_FILTER_CONFIG,
        USUARIOS_NON_FILTER_FIELDS
    )
    total = stmt.count()
    resp_value = stmt.order_by(UsuariosDB.id_usuario.asc()).offset(query.offset).limit(query.limit).all()
    return get_pagination_response(query.limit, query.offset, total, resp_value)

@router.post('/')
def post_usuarios(
    body: usuarios.UsuarioCreate,
    db: Session = DbSessionDep
):
    if isinstance(body, list):
        for usuario in body:
            db.add(UsuariosDB(**usuario.model_dump()))
    else:
        db.add(UsuariosDB(**body))
    db.commit()

@router.patch('/', response_model=usuarios.UsuarioCreate)
def patch_categorias(
    id_categoria: Annotated[int, Query(description="ID do usuário que será alterado")],
    body: usuarios.UsuarioCreate,
    db: Session = DbSessionDep
):
    dump_class = body.model_dump(exclude_unset=True)
    stmt = db.get(UsuariosDB, id_categoria)
    for k, val in dump_class.items():
        if hasattr(stmt, k):
            setattr(stmt, k, val)
    db.commit()    

@router.delete('/')
def delete_categorias(
    id_usuario: Annotated[int, Query(description="ID do usuário que será deletado")],
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    db.delete(stmt)
    db.commit()

@router.post('/{id_usuario}/add-endereco')
def add_endereco_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário que terá o endereço")],
    body: enderecos.EnderecoCreate,
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if len(stmt.enderecos) == 0:
        stmt = EnderecosDB(id_usuario_fk = id_usuario, padrao_endereco = True, **body.model_dump())
    else:
        stmt = EnderecosDB(id_usuario_fk = id_usuario, padrao_endereco = False, **body.model_dump())
    db.add(stmt)
    db.commit()

@router.post('/{id_usuario}/{id_endereco}')
def alter_endereco_padrao(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    id_endereco: Annotated[int, Path(description="Id do endereço")],
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    for endereco in stmt.enderecos:
        if endereco.id_endereco == id_endereco:
            endereco.padrao_endereco = True
        else:
            endereco.padrao_endereco = False
    db.commit()

@router.post('/{id_usuario}/add-telefone')
def add_telefones_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário que terá o endereço")],
    body: telefones.TelefoneCreate,
    db: Session = DbSessionDep
):
    stmt = TelefonesDB(id_usuario_fk = id_usuario, **body.model_dump())
    db.add(stmt)
    db.commit()

@router.post('/login', response_model=usuarios.UsuarioResponse|bool)
def verify_login(
    body: usuarios.UsuarioVerify,
    db: Session = DbSessionDep
):
    stmt = db.query(UsuariosDB).filter(UsuariosDB.email_usuario == body.email_usuario)
    db_usuario = stmt.first()
    if db_usuario is not None and verify_hash(body.senha_usuario, db_usuario.senha_usuario):
        return db_usuario
    else:
        return False
    
@router.post('/admin', response_model=usuarios.UsuarioResponse|bool)
def verify_admin(
    body: usuarios.UsuarioVerify,
    db: Session = DbSessionDep
):
    user_login = verify_login(body, db)
    if user_login and user_login.admin_usuario:
        return user_login
    else:
        return False