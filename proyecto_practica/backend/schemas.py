"""
El archivo models.py (SQLAlchemy) habla única y exclusivamente con PostgreSQL. 
A él no le importa qué te manda el usuario desde el navegador.
El archivo schemas.py (Pydantic) habla única y exclusivamente con Internet.
A él no le importa cómo se guardan los datos en el disco duro; su único trabajo es revisar la
mochila del usuario en la puerta de entrada (POST) o de salida (GET).
"""
from pydantic import BaseModel,Field
from typing import Optional, List

# 1. EL GUARDIA DE ENTRADA (Para POST y PUT)
# Lo que el usuario nos manda desde internet


# clase de usuarios
class UsuarioNuevo(BaseModel):
    nombre: str
    email: str
    password: str = Field(min_length=4, max_length=50)


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True


class ProductoNuevo(BaseModel):  # clase para agregar datos cualquiera que no cumpla no entra
    # antes aqui estaba el id lo quitamos pq postgres lo genera solo
    nombre: str
    categoria: str
    precio: float


# 2. EL GUARDIA DE SALIDA (Para GET)
# Lo que nosotros le mostramos al usuario en la pantalla
class Productorespuesta(BaseModel):
    id: int
    nombre:str
    precio:float
    dueño: Optional[UsuarioRespuesta] = None
    # 3. LA CONFIGURACIÓN MÁGICA DEL TRADUCTOR
    class Config:
        from_attributes = True #esto es para que pueda leer el orm 

# --- GUARDIAS DEL CARRITO Y PEDIDOS ---


# 1. Guardia de Entrada: Lo que trae el cliente en las manos (1 item)
class ItemCarrito(BaseModel):
    producto_id: int
    cantidad: int


# 2. Guardia de Entrada: El carrito completo (Una lista de items)
class PedidoNuevo(BaseModel):
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: str
    direccion: str
    detalles: List[ItemCarrito]


# 3. Guardia de Salida: Lo que le mostramos en la factura (Detalle)
class DetallePedidoRespuesta(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

    class Config:
        from_attributes = True


# 4. Guardia de Salida: La factura completa
class PedidoRespuesta(BaseModel):
    id: int
    usuario_id: Optional[int] = None
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: str
    direccion: str
    
    estado: str
    detalles: List[DetallePedidoRespuesta] = []  # Aquí anidamos la lista de ropa

    class Config:
        from_attributes = True
