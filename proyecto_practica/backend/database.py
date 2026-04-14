from sqlalchemy import create_engine 
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
# ejecutamos la llave: esto buscar el archivo en .env
load_dotenv()
# le pedimos a python que busque
sqlalchemy_Database_url = os.getenv(
    "DATABASE_URL"
)  
# Si por alguna razón no encuentra el archivo .env, lanzamos un error para darnos cuenta de inmediato
if sqlalchemy_Database_url is None:
    raise ValueError(
        "¡Peligro! No se encontró la URL de la base de datos en el archivo .env"
    )

# el motor
engine = create_engine(sqlalchemy_Database_url)


# la sesion
# autocommit = false porque nosotros decidimos cuando guardar por seguridad
sesionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# la base
base = declarative_base()




def get_db():
    db = sesionlocal()
    try:
        yield db  # 'yield' es como un 'return' que pausa la función. Entrega la sesión y se queda esperando.
    finally:
        db.close()  # Cuando la ruta web termina su trabajo, Python vuelve aquí y cierra la puerta.
