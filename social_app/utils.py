from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_pswd(user_password,hash_password):
    return pwd_context.verify(user_password, hash_password)
