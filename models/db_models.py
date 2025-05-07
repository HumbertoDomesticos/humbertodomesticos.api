from sqlalchemy import String, ForeignKey, create_engine, Float, Integer, DECIMAL
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
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
    preco_prod: Mapped[float] = mapped_column(DECIMAL(10, 2))
    desconto_prod: Mapped[int] = mapped_column(Integer, index=True)
    
    images_prod: Mapped[list["ImagesDB"]] = relationship()
    
    @validates("images_prod")
    def convert(self, _, value) -> ImagesDB:
        if value and isinstance(value, dict):
            return ImagesDB(**value)
        return value   
    
class UsuariosDB(Base):
    __tablename__ = 'usuarios'

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome_usuario: Mapped[str] = mapped_column(String(50))
    email_usuario: Mapped[str] = mapped_column(String(50))
    senha_usuario: Mapped[str] = mapped_column(String(50))

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