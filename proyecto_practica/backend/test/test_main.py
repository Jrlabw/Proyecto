from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db
import models

# 1. Creamos un motor para una base de datos temporal (SQLite es un archivo local ligero)
URL_BASE_DATOS_TEST = "sqlite:///./test_desechable.db"
motor_test = create_engine(
    URL_BASE_DATOS_TEST, connect_args={"check_same_thread": False}
)
SesionTest = sessionmaker(autocommit=False, autoflush=False, bind=motor_test)

# 2. Reseteamos la base de datos temporal (Borramos todo y creamos tablas limpias)
models.base.metadata.drop_all(bind=motor_test)
models.base.metadata.create_all(bind=motor_test)


# 3. El truco de magia: Reemplazamos el 'get_db' original por el temporal
def override_get_db():
    db = SesionTest()
    try:
        yield db
    finally:
        db.close()


# Le decimos a FastAPI que use nuestra función temporal en lugar de la original
app.dependency_overrides[get_db] = override_get_db


cliente = TestClient(app)


# 2. Las funciones de test SIEMPRE deben empezar con la palabra "test_"
def test_dar_bienvenida():

    # 3. El robot hace una petición GET a la ruta principal
    respuesta = cliente.get("/")

    # 4. LAS AFIRMACIONES (Asserts): Aquí evaluamos si el servidor hizo su trabajo

    # Afirmación A: El código de estado debe ser 200 (OK)
    assert respuesta.status_code == 200

    # Afirmación B: El JSON que devuelve debe ser exactamente este
    assert respuesta.json() == {
        "mensaje": "Bienvenido a mi tienda virtual",
        "estado": "online",
    }


def test_crear_usuario():
    # 1. El robot prepara la mochila de datos falsos (El JSON)
    datos_prueba = {
        "nombre": "Robot Tester",
        "email": "robot@tienda.com",
        "password": "password123",
    }

    # 2. El robot dispara la petición POST a la ruta de usuarios
    respuesta = cliente.post("/usuario/", json=datos_prueba)

    # 3. LAS AFIRMACIONES LÓGICAS

    # Afirmación A: El servidor debe responder que todo salió bien (200 OK)
    assert respuesta.status_code == 200

    # Afirmación B: El diccionario que devuelve el servidor debe tener el email correcto
    datos_devueltos = respuesta.json()
    assert datos_devueltos["email"] == "robot@tienda.com"

    # Afirmación C: Por seguridad, la contraseña NO debe venir en la respuesta
    assert "password" not in datos_devueltos


def test_login_y_crear_producto():

    # 1. El robot hace la fila en el Login.
    # OJO: Usamos 'data=' en lugar de 'json=' porque el Login exige Form Data.
    # Además, el estándar de seguridad exige que la llave se llame 'username', aunque sea un email.
    datos_login = {"username": "robot@tienda.com", "password": "password123"}
    respuesta_login = cliente.post("/login", data=datos_login)

    # Afirmamos que el cadenero lo dejó pasar (200 OK)
    assert respuesta_login.status_code == 200

    # 2. El robot agarra la pulsera VIP (el token)
    token = respuesta_login.json().get("access_token")

    # 3. El robot se pone la pulsera en las "Cabeceras" (Headers)
    # Así es como viajan los tokens por internet, con la palabra "Bearer " antes.
    cabeceras_vip = {"Authorization": f"Bearer {token}"}

    # 4. El robot intenta crear ropa enviando el JSON y mostrando las cabeceras
    nueva_camiseta = {
        "nombre": "Camiseta Robot",
        "categoria": "Ropa Tech",
        "precio": 99.99,
    }
    respuesta_producto = cliente.post(
        "/productos/", json=nueva_camiseta, headers=cabeceras_vip
    )

    # 5. LAS AFIRMACIONES FINALES
    assert respuesta_producto.status_code == 200
    assert respuesta_producto.json()["nombre"] == "Camiseta Robot"
