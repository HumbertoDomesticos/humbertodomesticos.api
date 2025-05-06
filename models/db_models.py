from sqlalchemy import String, ForeignKey, create_engine, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass
    
class ProdutosDB(Base):
    __tablename__ = 'produtos'

    id_prod: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome_prod: Mapped[str] = mapped_column(String(200))
    preco_prod: Mapped[float] = mapped_column(Float(2, True))
    desconto_prod: Mapped[int] = mapped_column(Integer, index=True)
    
connection_string = "mysql+mysqlconnector://root:root@localhost:3306/db_humb"
engine = create_engine(connection_string, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)