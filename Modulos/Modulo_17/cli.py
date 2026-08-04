import os

import httpx
import typer

# 1. VARIABLE DE ENTORNO: URL de la API (Si no existe en el sistema, usa localhost por defecto)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# 2. Inicializamos Typer (La magia de nuestra CLI)
app = typer.Typer(
    help="Herramienta de Consola para gestionar las Órdenes de la empresa."
)


# --- COMANDO 1: LISTAR ÓRDENES ---
@app.command("listar")
def listar_ordenes():
    """Descarga y muestra todas las órdenes desde la base de datos."""
    typer.secho(f"🌐 Conectando a {API_URL}...", fg=typer.colors.CYAN)

    try:
        # Hacemos la petición a la API del módulo 8
        respuesta = httpx.get(f"{API_URL}/orders")
        respuesta.raise_for_status()
        ordenes = respuesta.json()

        if not ordenes:
            typer.secho("📭 No hay órdenes registradas aún.", fg=typer.colors.YELLOW)
            return

        typer.secho("✅ ÓRDENES ENCONTRADAS:", fg=typer.colors.GREEN, bold=True)
        for ord in ordenes:
            typer.echo(
                f" - ID: {ord['id']} | Producto: {ord['producto']} | Cantidad: {ord['cantidad']}"
            )

    except httpx.ConnectError:
        typer.secho(
            "❌ Error: No se pudo conectar. ¿Olvidaste encender el servidor de la API del Módulo 8?",
            fg=typer.colors.RED,
        )


# --- COMANDO 2: CREAR UNA ORDEN ---
# Fíjate cómo Typer usa las anotaciones (int, str) para obligar al usuario a meter bien los datos
@app.command("crear")
def crear_orden(id_orden: int, producto: str, cantidad: int):
    """Crea una orden nueva. Ej: crear 5 'Monitor' 2"""

    # 1. Primero necesitamos la "pulsera VIP" (El login del módulo 8)
    try:
        login_res = httpx.post(
            f"{API_URL}/login", json={"username": "admin", "password": "secreto"}
        )
        login_res.raise_for_status()
        token = login_res.json()["access_token"]

        # 2. Con el token, intentamos crear la orden
        nueva_orden = {"id": id_orden, "producto": producto, "cantidad": cantidad}
        respuesta = httpx.post(
            f"{API_URL}/orders", json=nueva_orden, params={"token": token}
        )

        if respuesta.status_code == 201:
            typer.secho(
                f"✨ ¡Orden de '{producto}' creada exitosamente!", fg=typer.colors.GREEN
            )
        else:
            typer.secho(f"⚠️ Error al crear: {respuesta.text}", fg=typer.colors.RED)

    except httpx.ConnectError:
        typer.secho(
            "❌ Error de conexión. El servidor de la API parece estar apagado.",
            fg=typer.colors.RED,
        )


# Esto solo se usa si llamamos al archivo directamente
if __name__ == "__main__":
    app()
