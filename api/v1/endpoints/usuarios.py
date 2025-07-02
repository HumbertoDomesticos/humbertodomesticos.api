from fastapi import APIRouter, Query, Path, HTTPException
from database import DbSessionDep, Session
from typing import Dict, Tuple, List, Union, Annotated, Set

from core import apply_filters_from_model, get_pagination_response, PaginatedResponse, DEFAULT_NON_FILTER_FIELDS, verify_hash
from models.schemas import usuarios, telefones, enderecos
from models.db_models import UsuariosDB, TelefonesDB, EnderecosDB

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

USUARIOS_FILTER_CONFIG: Dict[str, Tuple[str, str]] = {
    "id_usuario": ("id_usuario", "eq"),
    "nome_usuario": ("nome_usuario", "contains"),
    "genero_usuario": ("genero_usuario", "eq"),
    "cpf_usuario": ("cpf_usuario", "eq")
}

USUARIOS_NON_FILTER_FIELDS: Set[str] = {"limit", "offset", "sort_by", "order_by", "telefones", "enderecos"}

@router.get('/',
            response_model=PaginatedResponse[usuarios.UsuarioResponse],
            description="Busca os usuários")
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

@router.post('/', 
             response_model=usuarios.UsuarioResponse,
             description="Cria um novo usuário")
def post_usuarios(
    body: usuarios.UsuarioCreate,
    db: Session = DbSessionDep
):
    db.add(UsuariosDB(**body.model_dump()))
    db.commit()
    stmt = db.query(UsuariosDB).order_by(UsuariosDB.id_usuario.desc()).limit(1)
    return stmt.first()

@router.patch('/', 
              response_model=usuarios.UsuarioResponse,
              description="Altera os dados de um usuário")
def patch_usuario(
    id_usuario: Annotated[int, Query(description="ID do usuário que será alterado")],
    body: usuarios.UsuarioCreate,
    db: Session = DbSessionDep
):
    dump_class = body.model_dump(exclude_unset=True)
    stmt = db.get(UsuariosDB, id_usuario)
    if not stmt:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    for k, val in dump_class.items():
        if hasattr(stmt, k):
            setattr(stmt, k, val)
    
    db.commit()
    db.refresh(stmt)
    return stmt

@router.delete('/', 
               response_model=str,
               description="Deleta um usuário")
def delete_usuario(
    id_usuario: Annotated[int, Query(description="ID do usuário que será deletado")],
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if not stmt:
        return f"Usuário com id: {id_usuario} não encontrado"
    db.delete(stmt)
    db.commit()
    return f"Usuário com id: {id_usuario} foi removido"

@router.post('/{id_usuario}/add-endereco',
             response_model=usuarios.UsuarioResponse|bool,
             description="Adiciona um endereço do usuário")
def add_endereco_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário que terá o endereço")],
    body: enderecos.EnderecoCreate,
    db: Session = DbSessionDep
):
    usuario = db.get(UsuariosDB, id_usuario)
    if usuario is None:
        return False
    
    # Verifica se já existe algum endereço padrão
    has_padrao = any(endereco.padrao_endereco for endereco in usuario.enderecos)
    
    # Cria novo endereço
    novo_endereco = EnderecosDB(
        id_usuario_fk=id_usuario,
        padrao_endereco=not has_padrao,
        **body.model_dump()
    )
    
    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)
    return usuario

@router.post('/{id_usuario}/{id_endereco}',
             response_model=usuarios.UsuarioResponse|bool,
             description="Torna um endereço em padrão")
def alter_endereco_padrao(
    id_usuario: Annotated[int, Path(description="Id do usuário")],
    id_endereco: Annotated[int, Path(description="Id do endereço")],
    db: Session = DbSessionDep
):
    stmt = db.get(UsuariosDB, id_usuario)
    if stmt is None:
        return False
    for endereco in stmt.enderecos:
        if endereco.id_endereco == id_endereco:
            endereco.padrao_endereco = True
        else:
            endereco.padrao_endereco = False
    db.commit()
    db.refresh(stmt)
    return stmt

@router.post('/{id_usuario}/telefones',
             response_model=usuarios.UsuarioResponse,
             description="Adiciona um telefone ao usuário")
def add_telefone_usuario(
    id_usuario: Annotated[int, Path(description="Id do usuário que terá o telefone")],
    body: telefones.TelefoneCreate,
    db: Session = DbSessionDep
):
    usuario = db.get(UsuariosDB, id_usuario)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    novo_telefone = TelefonesDB(
        id_usuario_fk=id_usuario,
        **body.model_dump()
    )
    
    db.add(novo_telefone)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.post('/login', 
             response_model=usuarios.UsuarioResponse|bool,
             description="Tenta fazer o login do usuário")
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
    
@router.post('/admin', 
             response_model=usuarios.UsuarioResponse|bool,
             description="Tenta fazer login como admin")
def verify_admin(
    body: usuarios.UsuarioVerify,
    db: Session = DbSessionDep
):
    user_login = verify_login(body, db)
    if user_login and user_login.admin_usuario:
        return user_login
    else:
        return False