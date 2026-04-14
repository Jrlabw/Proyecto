# importamos ahora nuestros archivos
import models
from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, pedidos, productos, usuarios

"""
Ahora que tienes los 3 archivos base (el Cuarto de Máquinas, el Espejo y el Guardia de Seguridad), vamos a limpiar tu main.py.
Este archivo ya no va a tener contraseñas, ni comandos SQL sucios, ni validaciones manuales. 
Su único trabajo será recibir al cliente, pedirle los datos a la base de datos a través del ORM, y devolverlos.
 """



models.base.metadata.create_all(bind=engine)

app = FastAPI()  # Inicio del server

origenes_permitidos = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# añadimos las otras rutas
app.include_router(productos.router)
app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(pedidos.router)




# creacion de la url "pagina principal"
@app.get("/")
def dar_bienvenida():
    return {"mensaje": "Bienvenido a mi tienda virtual", "estado": "online"}
