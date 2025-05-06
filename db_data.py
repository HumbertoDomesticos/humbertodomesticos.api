from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from models import db_models

db_models.Base.metadata.create_all(bind=db_models.engine)

def get_db():
    db = db_models.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]