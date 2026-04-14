from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# importar de nuevo las herramientas
import models
import schemas
import routers.authAdm as authAdm
from database import get_db

# jefe de productos
router = APIRouter(prefix="/productos", tags=["Productos"])



@router.post("/", response_model=schemas.Productorespuesta)
def agregar_producto(producto: schemas.ProductoNuevo, db: Session = Depends(get_db), usuario_actual: int = Depends(authAdm.obtener_usuario_actual)):
    # creamos el objeto orm pasando los datos que valido pydantic
    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        dueño_id=usuario_actual,
    )

    # lo preparamos en la sesion
    db.add(nuevo_producto)
    # lo guardamos en postgres
    db.commit()

    # traemos el id que postgres le acaba de asignar
    db.refresh(nuevo_producto)
    # devolvemos el producto completo
    return nuevo_producto



@router.get("/inventario", response_model=list[schemas.Productorespuesta])
# aqui usamos el guardia de seguridad de salida para que sepa que tiene que devolver
def ver_inventario(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):  # el depende sirve para inyeccion de dependencias en lugar de abrir la sesion manualmente
    # como antes con el cursor ahora sirve para tener la ruta y obtener una sesion en la base de datos
    # db.query() es el equivalente ORM a "SELECT * FROM productos;"
    productos_db = (
        db.query(models.Producto).offset(skip).limit(limit).all()
    )  # ahora el orm aqui traduce todo
    return productos_db


@router.get("/{producto_id}", response_model=schemas.Productorespuesta)
# igual que antes pero ahora agregamos el response model para que nos tenga que devolver ese modelo
def encontrar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = (
        db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    )
    # ahora la query es de esta forma con el orm el filtro y el first para obtener nomas el primer dato
    if producto == None:
        raise HTTPException(status_code=404, detail="El producto no existe")

    return producto  # retornamos el producto


# funcion para eliminar producto
@router.delete("/{producto_id}")
def borrar_producto(producto_id: int, db: Session = Depends(get_db), usuario_actual:int = Depends(authAdm.obtener_usuario_actual)):
    producto_a_borrar = encontrar_producto(
        producto_id, db
    )  # esto sirve pq reutilizamos la otra funcion que yaa si no se completa no llegaria aca

    #blindaje 
    if producto_a_borrar.dueño_id != usuario_actual:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para borrar ese producto")    
    db.delete(producto_a_borrar)
    db.commit()
    return {"mensaje": "producto eliminado exitosamente"}


# funcion para actualizar productos
@router.put("/{producto_id}", response_model=schemas.Productorespuesta)
def actualizar_producto(
    producto_id: int, datos_nuevo: schemas.ProductoNuevo, db: Session = Depends(get_db), 
    usuario_actual:int = Depends(authAdm.obtener_usuario_actual)
):
    producto_actualizar: models.Producto = encontrar_producto(producto_id, db)
    #  El Blindaje: Verificamos que no edite ropa ajena
    if int(producto_actualizar.dueño_id) != usuario_actual:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este producto",
        )

    producto_actualizar.nombre = datos_nuevo.nombre
    producto_actualizar.precio = datos_nuevo.precio
    producto_actualizar.categoria = datos_nuevo.categoria

    db.commit()
    db.refresh(producto_actualizar)
    return producto_actualizar
