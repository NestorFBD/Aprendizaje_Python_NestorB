from pathlib import Path

import joblib  # type: ignore
import pandas as pd  # type: ignore
from sklearn.metrics import accuracy_score  # type: ignore
from sklearn.tree import DecisionTreeClassifier  # type: ignore

# Configuramos rutas universales
CARPETA = Path(__file__).parent
ARCHIVO_CSV = CARPETA / "datos_clientes.csv"
ARCHIVO_MODELO = CARPETA / "modelo_clasificador.joblib"


def crear_datos_de_prueba() -> None:
    """Crea un CSV simulado de clientes para nuestro laboratorio."""
    datos = {
        "edad": [25, 45, 30, 50, 23, 40, None, 55, 28, 35],
        "salario_miles": [30, 80, 45, 120, 25, 70, 60, 150, 40, 65],
        "compro_producto": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # 0 = No, 1 = Sí
    }
    df = pd.DataFrame(datos)
    df.to_csv(ARCHIVO_CSV, index=False)
    print("1. ✅ Archivo CSV de prueba creado.")


def entrenar_y_guardar_modelo() -> None:
    """Carga datos, los limpia, entrena la IA y la guarda en el disco."""
    # 1. Cargar datos
    df = pd.read_csv(ARCHIVO_CSV)

    # 2. Limpieza básica (Llenar nulos con el promedio)
    df.fillna(df.mean(), inplace=True)

    # 3. Separar Características (X) y el Objetivo a predecir (y)
    X = df[["edad", "salario_miles"]]
    y = df["compro_producto"]

    # 4. Entrenar el modelo (Un Árbol de Decisión sencillo)
    modelo = DecisionTreeClassifier(random_state=42)
    modelo.fit(X, y)

    # Verificamos qué tan bueno es con los mismos datos
    precision = accuracy_score(y, modelo.predict(X))
    print(f"2. 🧠 Modelo entrenado con una precisión del {precision * 100}%")

    # 5. Serialización (Congelar el cerebro en un archivo)
    joblib.dump(modelo, ARCHIVO_MODELO)
    print(f"3. 💾 Modelo guardado exitosamente en {ARCHIVO_MODELO.name}")


def hacer_inferencia(edad: float, salario: float) -> None:
    """Carga el modelo del disco duro y predice sobre un cliente NUEVO."""
    print(
        f"\n--- INFERENCIA PARA NUEVO CLIENTE (Edad: {edad}, Salario: {salario}k) ---"
    )

    # 1. Cargar el modelo serializado
    modelo_cargado = joblib.load(ARCHIVO_MODELO)

    # 2. Formatear los datos como los espera Pandas (un DataFrame de 1 fila)
    nuevos_datos = pd.DataFrame([{"edad": edad, "salario_miles": salario}])

    # 3. Predecir
    prediccion = modelo_cargado.predict(nuevos_datos)

    if prediccion[0] == 1:
        print("🔮 Predicción: ¡Este cliente SÍ comprará el producto! 🛒")
    else:
        print("🔮 Predicción: Este cliente NO comprará el producto. ❌")


def main() -> None:
    # Ejecutamos el pipeline completo
    crear_datos_de_prueba()
    entrenar_y_guardar_modelo()

    # Simulamos que llega un cliente nuevo (Ej. Joven con bajo salario)
    hacer_inferencia(edad=22, salario=30)

    # Simulamos que llega otro cliente (Ej. Adulto con alto salario)
    hacer_inferencia(edad=44, salario=100)


if __name__ == "__main__":
    main()
