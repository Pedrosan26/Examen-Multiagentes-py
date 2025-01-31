import socket
import json
import threading

class SocketServer:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.lock = threading.Lock()  # Para proteger el acceso a las conexiones en un entorno multihilo

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            conn, addr = self.server.accept()
            with self.lock:
                self.connections.append(conn)
            print(f"Conexión establecida con {addr}")
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)  # Recibe los datos del cliente
                if not data:
                    break  # Si no hay datos, se termina la conexión
                print(f"Datos recibidos de {addr}: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Error con el cliente {addr}: {e}")
        finally:
            with self.lock:
                self.connections.remove(conn)
            conn.close()
            print(f"Conexión cerrada con {addr}")

    def send_data(self, data):
        # Serializa el JSON a una cadena y lo envía a todos los clientes conectados
        serialized = json.dumps(data).encode('utf-8')
        with self.lock:
            for conn in self.connections:
                try:
                    conn.sendall(serialized + b'\n')  # Envía el JSON seguido de una nueva línea
                except Exception as e:
                    print(f"Error al enviar datos a un cliente: {e}")
                    self.connections.remove(conn)
                    conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    server = SocketServer()
    server.start()
    server.send_data({"mensaje": "Hola a todos los clientes"})
