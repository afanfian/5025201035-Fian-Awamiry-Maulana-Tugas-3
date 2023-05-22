import socket
import threading
import logging
import time

class ClientProcessor(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        while True:
            data = self.connection.recv(32)
            if not data:
                break
            logging.warning(f"[TIME SERVER] received {data} from {self.address}")
            # Diawali dengan string “TIME dan diakhiri dengan karakter 13 dan karakter 10”
            if data.startswith(b'TIME') and data.endswith(b'\r\n'):
                # <jam> berisikan info jam dalam format “hh:mm:ss” dan diakhiri dengan karakter 13 dan karakter 10
                request_time = time.strftime("%H:%M:%S")
                # Diawali dengan “JAM<spasi><jam>”
                response = f"JAM {request_time}\r\n"
                logging.warning(f"[TIME SERVER] sending {response} to {self.address}")
                # Dalam bentuk string (UTF-8)
                self.connection.sendall(response.encode('utf-8'))
            else:
                break

        self.connection.close()

class TimeServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        while True:
            connection, client_address = self.my_socket.accept()
            logging.warning(f"connection from {client_address}")

            client_processor = ClientProcessor(connection, client_address)
            client_processor.start()
            self.clients.append(client_processor)

    def stop(self):
        self.my_socket.close()

def main():
    logging.basicConfig(level=logging.WARNING)
    server = TimeServer()
    server.start()
    server.join()

if __name__ == "__main__":
    main()