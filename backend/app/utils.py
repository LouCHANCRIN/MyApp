from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(string: str) -> str:
    return pwd_context.hash(string)


def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)