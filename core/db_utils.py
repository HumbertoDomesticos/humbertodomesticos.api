from sqlalchemy import Column, and_
from sqlalchemy.orm import Query
from pydantic import BaseModel
from typing import Any, Callable, Dict, Set, Tuple
import toml

"""
Dicionário com todos operadores que serão usados no SQL pelo SQLAlchemy 
"""
OPERATORS: Dict[str, Callable[[Column, Any], Any]] = {
    "eq": lambda col, val: col == val, 
    "ne": lambda col, val: col != val, 
    "lt": lambda col, val: col < val, 
    "lte": lambda col, val: col <= val,
    "gt": lambda col, val: col > val, 
    "gte": lambda col, val: col >= val,
    "in": lambda col, val: col.in_(val),
    "notin": lambda col, val: col.notin_(val),
    "like": lambda col, val: col.like(val),
    "ilike": lambda col, val: col.ilike(val),
    "contains": lambda col, val: col.contains(val),
    "icontains": lambda col, val: col.ilike(f"%{val}%"),
    "startswith": lambda col, val: col.startswith(val),
    "istartswith": lambda col, val: col.ilike(f"{val}%"),
    "endswith": lambda col, val: col.endswith(val),
    "iendswith": lambda col, val: col.ilike(f"%{val}"),
    "isnull": lambda col, val: col.is_(None) if val is True else col.isnot(None)
}

DEFAULT_NON_FILTER_FIELDS: Set[str] = {"limit", "offset", "sort_by", "order_by"}

def apply_filters_from_model(
    db_query: Query,
    db_model_cls: Any,
    pydantic_query_instance: BaseModel,
    filter_config: Dict[str, Tuple[str, str]],
    non_filter_fields: Set[str] = DEFAULT_NON_FILTER_FIELDS
) -> Query:
    """
        Função que retorna as condições aplicadas para busca pelo SQL
    """
    active_filters = pydantic_query_instance.model_dump(exclude_none=True)
    conditions = []
    
    for pydantic_field_name, value in active_filters.items():
        if pydantic_field_name in non_filter_fields:
            continue
        
        if pydantic_field_name in filter_config:
            column_name, operator_key = filter_config[pydantic_field_name]
            
            if not hasattr(db_model_cls, column_name):
                print(f"Aviso: Coluna '{column_name}' não encontrado no modelo DB para o campo pydantic '{pydantic_field_name}'")
                continue
        
            column: Column = getattr(db_model_cls, column_name)
            
            if operator_key in OPERATORS:
                op_func = OPERATORS[operator_key]
                conditions.append(op_func(column, value))
            else:
                print(f"Aviso: operador desconhecido '{operator_key}' para o campo pydantic '{pydantic_field_name}'")
            
    if conditions:
        return db_query.filter(and_(*conditions))
    return db_query

def get_conn_string(dbms_type: str = 'mysql') -> str:
    """
        Função que constrói a string de conexão usando os dados em 'pyconfig.toml'
    """
    config = toml.load("pyconfig.toml")["database_conn"]
    if dbms_type == 'mysql':
        driver = config['driver'][1]
    elif dbms_type == 'postgresql':
        driver = config['driver'][0]  
    else:
        raise Exception()
    return f"{driver}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db_name']}"