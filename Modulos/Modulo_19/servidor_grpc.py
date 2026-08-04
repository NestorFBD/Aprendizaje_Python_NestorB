import json
from concurrent import futures

import grpc

# Importamos los "Stubs" autogenerados
import ordenes_pb2
import ordenes_pb2_grpc
import redis  # type: ignore


class GestorOrdenesServicer(ordenes_pb2_grpc.GestorOrdenesServicer):
    """Aquí implementamos la lógica de nuestro contrato."""

    def __init__(self):
        # Preparamos la conexión a Redis (El buzón de correos)
        # Usamos try-except por si no tienes Redis instalado en tu PC, para que no explote
        try:
            self.buzon = redis.Redis(host="localhost", port=6379, decode_responses=True)
            self.buzon.ping()  # Probamos conexión
            self.tiene_redis = True
        except redis.ConnectionError:
            self.tiene_redis = False

    def CrearOrden(self, request, context):
        print(
            f"\n⚙️ [Servidor] Recibida petición gRPC: {request.producto} por ${request.monto}"
        )

        # 1. Lógica de negocio (simulada)
        nuevo_id = f"ORD-{int(request.monto)}"

        # 2. Publicamos el Evento de Dominio en el Buzón (RabbitMQ / Redis)
        evento = {
            "evento": "OrderCreated",
            "id": nuevo_id,
            "producto": request.producto,
        }

        if self.tiene_redis:
            self.buzon.publish("canal_ordenes", json.dumps(evento))
            print(f"📢 [Mensajería] Evento publicado en Redis: {evento}")
        else:
            print(
                f"📢 [Mensajería] (Simulado) Evento publicado: {evento} (No hay Redis local)"
            )

        # 3. Respondemos usando el formato binario exacto del contrato
        return ordenes_pb2.OrdenResponse(
            id=nuevo_id, mensaje="Orden procesada a la velocidad de la luz"
        )


def iniciar_servidor():
    # Creamos el servidor gRPC usando el paralelismo del Módulo 10
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ordenes_pb2_grpc.add_GestorOrdenesServicer_to_server(
        GestorOrdenesServicer(), servidor
    )

    # Lo encendemos en el puerto 50051 (El puerto clásico de gRPC)
    servidor.add_insecure_port("[::]:50051")
    print("🚀 Servidor gRPC iniciado en el puerto 50051. Esperando conexiones...")
    servidor.start()
    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar_servidor()
