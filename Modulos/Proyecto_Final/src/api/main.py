from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.api.schemas import OrderCreate, OrderResponse, Token
from src.api.security import create_access_token, verify_token
from src.application.use_cases import OrderService

# Importamos nuestras capas
from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories import SQLAlchemyOrderRepository

app = FastAPI(title="API del Proyecto Final (Arquitectura Hexagonal). Nestor Becerra")


# --- INYECCIÓN DE DEPENDENCIAS (Wiring) ---
def get_order_service():
    """Conecta los cables: Base de Datos -> Repositorio -> Servicio"""
    db = SessionLocal()
    try:
        repo = SQLAlchemyOrderRepository(db)
        yield OrderService(repository=repo)
    finally:
        db.close()


# --- ENDPOINTS (Las Rutas) ---


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Puerta de entrada. (Usuario: admin, Clave: secreto)"""
    if form_data.username == "admin" and form_data.password == "secreto":
        token = create_access_token(form_data.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")


@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order_in: OrderCreate,
    service: OrderService = Depends(get_order_service),
    username: str = Depends(verify_token),  # ¡El guardia de seguridad!
):
    """Crea una orden (Solo con Token válido)"""
    new_order = service.create_order(customer=order_in.customer, amount=order_in.amount)
    return new_order  # FastAPI lo convierte a OrderResponse automáticamente


@app.get("/orders", response_model=list[OrderResponse])
def get_orders(
    service: OrderService = Depends(get_order_service),
    username: str = Depends(verify_token),
):
    """Lista las órdenes (Solo con Token válido)"""
    return service.list_orders()
