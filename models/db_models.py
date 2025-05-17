from sqlalchemy import String, ForeignKey, create_engine, Float, Integer, DECIMAL, Table, Column, Date
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from typing import List

class Base(DeclarativeBase):
    pass

class ImagesDB(Base):
    __tablename__ = 'prod_images'

    id_image: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_prod_image: Mapped[int] = mapped_column(ForeignKey('produtos.id_prod'))
    path_image: Mapped[str] = mapped_column(String(500))
    
class ProdutosDB(Base):
    __tablename__ = 'produtos'

    id_prod: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome_prod: Mapped[str] = mapped_column(String(200))
    descricao_prod: Mapped[str] = mapped_column(String(2000))
    preco_prod: Mapped[float] = mapped_column(DECIMAL(10, 2))
    desconto_prod: Mapped[int] = mapped_column(Integer, index=True)
    estoque_prod: Mapped[int] = mapped_column()
    
    images_prod: Mapped[list["ImagesDB"]] = relationship()
    
    categorias: Mapped[List["CategoriasDB"]] = relationship("CategoriasDB", secondary="em_categoria", back_populates="produtos")
    
    @validates("images_prod")
    def convert(self, _, value) -> ImagesDB:
        if value and isinstance(value, dict):
            return ImagesDB(**value)
        return value   
    
class CategoriasDB(Base):
    __tablename__ = 'categorias'
    
    id_categoria: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    descritivo_categoria: Mapped[str] = mapped_column(String(50))
    
    produtos: Mapped[List[ProdutosDB]] = relationship(ProdutosDB, secondary="em_categoria", back_populates="categorias")
    
em_categoria = Table('em_categoria', Base.metadata,
    Column('id_categoria', Integer, ForeignKey('categorias.id_categoria'), primary_key=True),
    Column('id_produto', Integer, ForeignKey('produtos.id_prod'), primary_key=True)
)
    
class UsuariosDB(Base):
    __tablename__ = 'usuarios'

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome_usuario: Mapped[str] = mapped_column(String(50))
    cpf_usuario: Mapped[str] = mapped_column(String(11), default="00000000000")
    email_usuario: Mapped[str] = mapped_column(String(50))
    data_nasc_usuario: Mapped[Date] = mapped_column(Date)
    senha_usuario: Mapped[str] = mapped_column(String(1000))
    admin_usuario: Mapped[bool] = mapped_column(default=False)
    ativo_usuario: Mapped[bool] = mapped_column(default=True)

    # TODO Checar se essa será a estrutura usada

class CarrinhosDB(Base):
    __tablename__ = 'carrinhos'

    id_carrinho: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

class PedidosBD(Base):
    __tablename__ = 'pedidos'

    id_pedido: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_usuario_pedido: Mapped[int] = mapped_column(ForeignKey('usuarios.id_usuario')) 
    
connection_string = "mysql+mysqlconnector://root:root@localhost:3306/db_humb"
engine = create_engine(connection_string, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)