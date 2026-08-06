from fastapi.testclient import TestClient
from src.api.main import app

# Creamos un navegador falso
client = TestClient(app)


def test_login_success():
    """Simula hacer un login correcto y recibir la pulsera VIP (Token)."""
    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "secreto",
        },  # OAuth2 usa 'data', no 'json'
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    """Simula un hacker intentando entrar con clave equivocada."""
    response = client.post(
        "/login", data={"username": "admin", "password": "clave_falsa"}
    )
    assert response.status_code == 400


def test_create_order_with_token():
    """Flujo completo (E2E): Login -> Obtener Token -> Crear Orden."""
    # 1. Login
    login_res = client.post("/login", data={"username": "admin", "password": "secreto"})
    token = login_res.json()["access_token"]

    # 2. Crear Orden (con headers de seguridad)
    headers = {"Authorization": f"Bearer {token}"}
    nueva_orden = {
        "customer": "Empresa X",
        "amount": 2000.0,
    }  # Más de $1000 = Descuento

    response = client.post("/orders", json=nueva_orden, headers=headers)

    # Verificamos
    assert response.status_code == 201
    datos_respuesta = response.json()
    assert datos_respuesta["customer"] == "Empresa X"
    # Como era 2000, el Servicio le debió aplicar un 10% de descuento ($200)
    assert datos_respuesta["amount"] == 1800.0
