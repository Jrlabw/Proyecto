import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os 
from dotenv import load_dotenv
load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITH = 'HS256'
ACCES_TOKEN_EXPIRE_MINUTES = 30 #dura 30 min

def hashear(password: str) -> str:
    # bcrypt solo lee bytes por lo que pasaremos texto plano a bytes
    pwd_bytes = password.encode("utf-8")

    # generamos la encryptacion y hashing
    hash_bytes = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())

    return hash_bytes.decode("utf-8")


# verificar contraseña
def verificar(password_plana: str, password_hasheada: str) -> bool:
    # comparamos la contraseña que pone el usuario con la encryptada
    return bcrypt.checkpw(
        password_plana.encode("utf-8"), password_hasheada.encode("utf-8")
    )


def crear_token_sesion(data: dict):
    #hacemos copia de los datos para no modificar
    to_encode = data.copy()

    #calculamos hora de vencimiento
    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)

    #agregamos la fecha de expiracion a los datos bajo la clave estandar
    to_encode.update({"exp": expire})
    #fabricamos el token usando los datos
    token_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return token_jwt