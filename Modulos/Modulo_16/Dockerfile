# ==========================================
# ETAPA 1: BUILDER (La fábrica de construcción)
# ==========================================
FROM python:3.12-slim as builder

# Preparamos el entorno de trabajo temporal
WORKDIR /app

# Instalamos Poetry temporalmente
RUN pip install poetry poetry-plugin-export

# Copiamos nuestros archivos de dependencias
COPY pyproject.toml poetry.lock ./

# Le decimos a Poetry que exporte un requirements.txt normal para ahorrar espacio
RUN poetry export -f requirements.txt --output requirements.txt

# ==========================================
# ETAPA 2: PRODUCCIÓN (El contenedor final y ligero)
# ==========================================
FROM python:3.12-slim

# Carpeta final en el servidor
WORKDIR /app

# Copiamos SOLO la lista de dependencias de la etapa anterior (ahorra muchísimo espacio)
COPY --from=builder /app/requirements.txt .

# Instalamos las librerías sin la basura de construcción
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos nuestro código de la API (Simulando que lo tomamos del Módulo 8)
# Nota: En un proyecto real, aquí copiaríamos la carpeta de la app.
COPY ./Modulos/Modulo_8/main.py /app/main.py

# Exponemos el puerto 8000 para que el internet pueda entrar
EXPOSE 8000

# El comando de arranque para el servidor web en la nube
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]