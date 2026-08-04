import grpc
import ordenes_pb2
import ordenes_pb2_grpc


def hacer_peticion():
    print("🌐 [Cliente] Conectando al servidor gRPC...")

    # 1. Abrimos un canal de comunicación directo (Binario)
    with grpc.insecure_channel("localhost:50051") as canal:
        # 2. Creamos el Stub del cliente
        cliente = ordenes_pb2_grpc.GestorOrdenesStub(canal)

        # 3. Empaquetamos nuestra petición
        peticion = ordenes_pb2.OrdenRequest(producto="Silla Gamer", monto=250.50)

        # 4. Hacemos la llamada
        respuesta = cliente.CrearOrden(peticion)

        print(
            f"✅ [Cliente] Respuesta recibida: ID '{respuesta.id}' - Mensaje: '{respuesta.mensaje}'"
        )


if __name__ == "__main__":
    hacer_peticion()
