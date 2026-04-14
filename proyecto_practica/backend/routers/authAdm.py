from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import routers.utilidades as utilidades

# le decimos a fastapi para las entradas
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

# esta funcion es la del guardia
def obtener_usuario_actual(token: str = Depends(oauth_scheme)):
    #preparamos el mensaje de error si paso tiempo limite o si no tiene permisos
    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Pase no concedido o vencido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #el guardia toma el token y usa la key para intentar desencriptar
        paylodad = jwt.decode(token, utilidades.SECRET_KEY, algorithms=[utilidades.ALGORITH])

        #extrae el id del usuario 
        usuario_id = paylodad.get("usuario_id")
        #si el token no tiene id es falso
        if usuario_id is None:
            raise error_credenciales
    except JWTError:
        #si hubo error rebota
        raise error_credenciales
    #si todo bien devolver el usuario
    return usuario_id
