from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing import Annotated
from core import get_conn_string
import toml

SQLALCHEMY_DATABASE_URL = get_conn_string()

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=toml.load("pyconfig.toml")["database_conn"]["echo"])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSessionDep: Annotated[Session, Depends(get_db)] = Depends(get_db)