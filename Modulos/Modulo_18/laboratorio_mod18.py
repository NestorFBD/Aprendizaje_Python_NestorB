from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


# =========================================================
# 1. GESTIÓN DE SECRETOS CON PYDANTIC
# =========================================================
class ConfiguracionSegura(BaseSettings):
    """
    Pydantic leerá automáticamente el archivo .env y buscará estas variables.
    Si no las encuentra, el programa no arranca (¡Previene errores!).
    """

    db_usuario: str

    # SecretStr: Un tipo de dato especial que oculta la contraseña
    # si intentas imprimirla por error en la pantalla.
    db_contrasena: SecretStr

    # Le decimos dónde está nuestro archivo de secretos
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# =========================================================
# EJECUCIÓN DEL PROGRAMA
# =========================================================
def main() -> None:
    print("--- INICIANDO SISTEMA SEGURO ---")

    try:
        # Pydantic va al archivo .env y carga las variables de forma segura
        config = ConfiguracionSegura()  # type: ignore

        print("\n✅ Configuraciones cargadas con éxito.")
        print(f"👤 Usuario de BD: {config.db_usuario}")

        # ¡Magia! Si intentas imprimir la contraseña, Pydantic la censura (**********)
        print(f"🔑 Contraseña cargada (Censurada por Pydantic): {config.db_contrasena}")

        # Para usarla de verdad (ej. para conectarte a SQLAlchemy), tienes que pedirla explícitamente:
        # contraseña_real = config.db_contrasena.get_secret_value()

    except Exception as e:
        print(f"❌ Error de seguridad crítico: {e}")


if __name__ == "__main__":
    main()
