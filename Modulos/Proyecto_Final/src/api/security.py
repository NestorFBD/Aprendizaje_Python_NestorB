from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# La llave secreta (En la vida real iría en el .env del Módulo 18)
SECRET_KEY = "super_secreta_clave_para_proyecto_final_12345"
ALGORITHM = "HS256"

# Le dice a FastAPI dónde está la puerta de entrada (el login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(username: str) -> str:
    """Crea una pulsera VIP (Token) válida por 30 minutos."""
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    """El Guardia: Revisa la pulsera antes de dejarte pasar."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        return username
    except jwt.PyJWTError:
        raise credentials_exception
