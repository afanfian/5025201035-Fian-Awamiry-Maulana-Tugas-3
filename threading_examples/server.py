import socket
import threading
import logging
import time

class ClientProcessor(threading.Thread):
    def __init__(self, connection, address, server):
        self.connection = connection
        self.address = address
        self.server = server
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(32)
            if not data:
                break
            logging.warning(f"[CLIENT PROCESSOR] received {data} from {self.address}")
            # Diawali dengan string “TIME dan diakhiri dengan karakter 13 dan karakter 10”
            if data.startswith(b'TIME') and data.endswith(b'\r\n'):
                # <jam> berisikan info jam dalam format “hh:mm:ss” dan diakhiri dengan karakter 13 dan karakter 10
                request_time = time.strftime("%H:%M:%S")
                # Diawali dengan “JAM<spasi><jam>”
                response = f"JAM {request_time}\r\n"
                logging.warning(f"[TIME SERVER] sending {response} to {self.address}")
                # Dalam bentuk string (UTF-8)
                self.connection.sendall(response.encode('utf-8'))
                self.server.update_client_count()  # Memanggil fungsi update_client_count pada server
            else:
                break

        self.connection.close()

class TimeServer(threading.Thread):
    def __init__(self):
        self.clients = []  # Daftar klien yang terhubung
        self.client_count = 0  # Jumlah klien yang terhubung
        self.response_count = 0  # Jumlah response yang dikirimkan
        threading.Thread.__init__(self)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.bind(('0.0.0.0', 45000))  # Menghubungkan socket ke alamat dan port tertentu
            my_socket.listen(1)  # Melihat koneksi masuk dengan backlog 1
            while True:
                connection, client_address = my_socket.accept()  # Menerima koneksi baru
                logging.warning(f"New connection from {client_address}")

                client_processor = ClientProcessor(connection, client_address, self)  # Membuat instance ClientProcessor untuk setiap koneksi
                client_processor.start()  # Memulai thread ClientProcessor
                self.clients.append(client_processor)  # Menambahkan ClientProcessor ke daftar klien yang terhubung
                self.client_count += 1  # Menambahkan jumlah klien yang terhubung
                logging.warning(f"Total clients connected: {self.client_count}")

    def update_client_count(self):
        self.response_count += 1  # Menambahkan jumlah response yang dikirimkan
        logging.warning(f"Total responses sent: {self.response_count}")

    def stop(self):
        # Tambahkan log di sini jika diperlukan sebelum menutup socket
        self.my_socket.close()

def main():
    logging.basicConfig(level=logging.WARNING)
    server = TimeServer()
    server.start()
    server.join()

if __name__ == "__main__":
    main()
