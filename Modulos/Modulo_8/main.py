from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

# Configuramos nuestra API y CORS básico
app = FastAPI(title="API de Órdenes", description="Mi primera API con FastAPI")

SECRET_KEY = "mi_clave_super_secreta_muy_larga_y_segura_123"  # Para firmar el Token JWT


# --- ESQUEMAS PYDANTIC (Los filtros de datos del Módulo 3) ---
class UserLogin(BaseModel):
    username: str
    password: str


class Order(BaseModel):
    id: int
    producto: str
    cantidad: int


class Token(BaseModel):
    access_token: str
    token_type: str


# --- BASE DE DATOS TEMPORAL EN MEMORIA ---
db_ordenes: list[Order] = []


# --- DEPENDENCIA: Validar la Pulsera VIP (JWT) ---
def verificar_token(token: str) -> str:
    """Revisa que el token sea válido antes de dejar pasar al usuario."""
    try:
        # Intentamos decodificar la pulsera
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]  # Devolvemos el nombre del usuario
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token expiró")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# --- ENDPOINTS (Las Rutas de la API) ---


@app.post("/login", response_model=Token)
def login(user: UserLogin) -> dict[str, str]:
    """Valida al usuario y le entrega su JWT."""
    if user.username == "admin" and user.password == "secreto":
        # Creamos el Token con duración de 30 minutos
        expiracion = datetime.now(UTC) + timedelta(minutes=30)
        datos = {"sub": user.username, "exp": expiracion}
        token_jwt = jwt.encode(datos, SECRET_KEY, algorithm="HS256")

        return {"access_token": token_jwt, "token_type": "bearer"}

    # Si la contraseña está mal, lanzamos error 401 (No autorizado)
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def crear_orden(orden: Order, token: str = Depends(verificar_token)) -> Order:
    """Crea una orden NUEVA (¡Solo si el token es válido!)"""
    db_ordenes.append(orden)
    return orden


@app.get("/orders", response_model=list[Order])
def leer_ordenes() -> list[Order]:
    """Cualquiera puede ver la lista de órdenes."""
    return db_ordenes
