from typing import Optional

def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}