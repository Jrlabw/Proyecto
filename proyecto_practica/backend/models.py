"""
El archivo models.py (SQLAlchemy) habla única y exclusivamente con PostgreSQL.
A él no le importa qué te manda el usuario desde el navegador.
El archivo schemas.py (Pydantic) habla única y exclusivamente con Internet.
A él no le importa cómo se guardan los datos en el disco duro; su único trabajo es revisar la
mochila del usuario en la puerta de entrada (POST) o de salida (GET).
"""

# primero necesitamos traer las herramientas del libro de registro (base)
# Traemos de SQLAlchemy los tipos de datos y la herramienta para crear columnas
from sqlalchemy import Float, Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Traemos nuestro Libro de Registro desde el archivo que acabas de crear
from database import base

class Usuario(base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True,index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# ahora creamos la clase producto que es el hijo de la base
class Producto(
    base
):  # aqui en python la herenciaa se maneja poniendo al padre entre parentesis
    # le decimos a sqlalchemy como se llama la tabla real en postgres
    __tablename__ = "productos"  # esto es obligatorio
    # definimos las columnas
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    # el column avisa que no es una variable normal si no una columna
    dueño_id = Column(Integer, ForeignKey("usuarios.id"))
    dueño = relationship("Usuario")



class Pedido(base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)

    # 1. Ahora el usuario_id es OPCIONAL (nullable=True) por si en el futuro agregas cuentas
    usuario_id = Column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=True
    )


    nombre_cliente = Column(String, nullable=False)
    email_cliente = Column(String, nullable=False)
    telefono_cliente = Column(String, nullable=False)
    direccion = Column(String, nullable=False)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="pendiente")

    cliente = relationship("Usuario")
    detalles = relationship("DetallePedido", back_populates="pedido")



class DetallePedido(base):
    __tablename__ = "detalles_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(
        Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False
    )
    producto_id = Column(
        Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False
    )

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)  # El precio congelado en el tiempo

    # Relaciones inversas
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")
