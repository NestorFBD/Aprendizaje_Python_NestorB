from fastapi.testclient import TestClient
from main import app

# Creamos un cliente falso para no tener que abrir el navegador
cliente = TestClient(app)


def test_flujo_completo_api() -> None:
    # 1. Intentamos hacer login
    respuesta_login = cliente.post(
        "/login", json={"username": "admin", "password": "secreto"}
    )
    assert (
        respuesta_login.status_code == 200
    )  # Verificamos que todo salió bien (HTTP 200)

    # Extraemos la pulsera (Token)
    token = respuesta_login.json()["access_token"]

    # 2. Intentamos crear una orden usando el Token
    nueva_orden = {"id": 1, "producto": "Laptop", "cantidad": 2}
    respuesta_crear = cliente.post(
        "/orders",
        json=nueva_orden,
        params={"token": token},  # Pasamos el token como seguridad
    )
    assert respuesta_crear.status_code == 201  # HTTP 201 = Creado

    # 3. Leemos las órdenes para ver si se guardó
    respuesta_leer = cliente.get("/orders")
    assert len(respuesta_leer.json()) == 1  # Verificamos que la lista tenga 1 orden
    assert respuesta_leer.json()[0]["producto"] == "Laptop"
