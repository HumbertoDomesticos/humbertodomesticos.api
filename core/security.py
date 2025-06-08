from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt", "sha512_crypt"],
    deprecated="auto"
)

def verify_hash(plain_text: str, hashed_text: str) -> bool:
    try:
        return pwd_context.verify(plain_text, hashed_text)
    except Exception:
        return False
    
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_sha_hash(plain_text: str) -> str:
    handler_sha512 = pwd_context.handler('sha512_crypt')
    return handler_sha512.hash(plain_text)