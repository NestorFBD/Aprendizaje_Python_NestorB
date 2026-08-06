from pydantic import BaseModel


class OrderCreate(BaseModel):
    """Caja de entrada: Lo que el usuario debe enviarnos."""

    customer: str
    amount: float


class OrderResponse(BaseModel):
    """Caja de salida: Lo que le mostramos al usuario."""

    id: str
    customer: str
    amount: float
    status: str


class Token(BaseModel):
    access_token: str
    token_type: str
