from typing import Optional

def convert_to_option(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}