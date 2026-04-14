from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# importamos herraminetas
import models
import schemas
from database import get_db
import routers.authAdm as authAdm
import routers.utilidades as utilidades

# jefe de departamento
router = APIRouter(
    prefix="/usuario",  # ahora todas las rutas empiezan con usuario
    tags=["Usuarios"],  # esto organiza el swagger en bloques bonitos
)


# ahora post para usuario (crear uusuario)
@router.post("/", response_model=schemas.UsuarioRespuesta)
def agregar_usuario(usuario: schemas.UsuarioNuevo, db: Session = Depends(get_db)):
    # lo mismo que en productos creamos el nuevo usuario
    contraseña_encryptada = utilidades.hashear(usuario.password)
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre, email=usuario.email, password=contraseña_encryptada
    )

    db.add(nuevo_usuario)

    db.commit()

    db.refresh(nuevo_usuario)
    return nuevo_usuario


# funcion para encontrar usuario
@router.get("/{usuario_id}", response_model=schemas.UsuarioRespuesta)
def encontrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return usuario


# funcion eliminar usuario
@router.delete("/{usuario_id}")
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db), usuario_actual:int = Depends(authAdm.obtener_usuario_actual)):
    if usuario_id != usuario_actual:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar usuario")
    
    usuario_borrar = encontrar_usuario(usuario_id, db)

    db.delete(usuario_borrar)
    db.commit()
    return {"mensaje": "usuario eliminado exitosamente"}


# funcion actualizar usuario
@router.put("/{usuario_id}", response_model=schemas.UsuarioRespuesta)
def actualizar_usuario(
    usuario_id: int, usuario_nuevo: schemas.UsuarioNuevo, db: Session = Depends(get_db),
    usuario_actual:int = Depends(authAdm.obtener_usuario_actual)
):
    if usuario_id != usuario_actual:
        raise HTTPException(status_code=403, detail="No tienes permiso")
    usuario_actualizar: models.Usuario = encontrar_usuario(usuario_id, db)

    usuario_actualizar.nombre = usuario_nuevo.nombre
    usuario_actualizar.email = usuario_nuevo.email
    usuario_actualizar.password = utilidades.hashear(usuario_nuevo.password)

    db.commit()
    db.refresh(usuario_actualizar)
    return usuario_actualizar
