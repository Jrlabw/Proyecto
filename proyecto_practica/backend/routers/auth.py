from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from routers import utilidades
import database, models

# Creamos el router (la oficina del cadenero)
router = APIRouter(tags=["Autenticación"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # 1. El cadenero busca al usuario en la base de datos por su email.
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == user_credentials.username)
        .first()
    )

    # 2. Si el usuario no existe en la base de datos...
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales inválidas"
        )

    # 3. Si existe, verificamos que la contraseña que escribió coincida con el hash de la base de datos
    if not utilidades.verificar(user_credentials.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales inválidas"
        )

    # 4. Si pasó las dos pruebas, ¡fabricamos su pase VIP!
    # Guardamos su ID dentro del token para saber quién es en el futuro
    token_jwt = utilidades.crear_token_sesion(data={"usuario_id": usuario.id})

    # 5. Le entregamos el token
    return {"access_token": token_jwt, "token_type": "bearer"}
