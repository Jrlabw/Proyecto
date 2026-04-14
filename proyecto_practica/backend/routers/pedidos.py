from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import routers.authAdm as authAdm
from database import get_db


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=schemas.PedidoRespuesta)
def crear_pedido(
    pedido_cliente: schemas.PedidoNuevo,
    db: Session = Depends(get_db)
):

    # Usamos el guardia para saber de quién es el pedido
    nuevo_pedido = models.Pedido(
        nombre_cliente=pedido_cliente.nombre_cliente,
        email_cliente=pedido_cliente.email_cliente,
        telefono_cliente=pedido_cliente.telefono_cliente,
        direccion=pedido_cliente.direccion
        # El usuario_id se queda vacío automáticamente
    ) # Refrescamos para que Postgres nos devuelva el ID del pedido (ej. Factura #1)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    for item in pedido_cliente.detalles:


        producto_db = (
            db.query(models.Producto)
            .filter(models.Producto.id == item.producto_id)
            .first()
        )

        if not producto_db:

            raise HTTPException(
                status_code=404,
                detail=f"El producto con ID {item.producto_id} no existe",
            )


        nuevo_detalle = models.DetallePedido(
            pedido_id=nuevo_pedido.id,  # Lo conectamos a la factura #1
            producto_id=item.producto_id,  # ID de la camiseta
            cantidad=item.cantidad,  # Cuántas quiere
            precio_unitario=producto_db.precio,  # ¡El precio real sacado de TU base de datos!
        )
        db.add(nuevo_detalle)


    db.commit()
    db.refresh(
        nuevo_pedido
    )  # Actualizamos la factura para que incluya todos los detalles

    # Devolvemos la factura completa
    return nuevo_pedido
