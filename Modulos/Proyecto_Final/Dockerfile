# ==========================================
# ETAPA 1: BUILDER (Fábrica)
# ==========================================
FROM python:3.12-slim as builder
WORKDIR /app

# Instalamos poetry y su accesorio (la lección que aprendimos en el Módulo 16)
RUN pip install poetry poetry-plugin-export

# Copiamos la configuración desde la raíz
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

# ==========================================
# ETAPA 2: PRODUCCIÓN (Contenedor final ultra-ligero)
# ==========================================
FROM python:3.12-slim
WORKDIR /app

# Copiamos solo los requirements para que sea liviano
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo nuestro proyecto final
COPY ./Proyecto_Final /app/Proyecto_Final

# Nos movemos a la carpeta del proyecto para que FastAPI encuentre la carpeta 'src'
WORKDIR /app/Proyecto_Final

EXPOSE 8000

# El comando de arranque para la web
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]