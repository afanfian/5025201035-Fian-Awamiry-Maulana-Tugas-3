import socket
import logging
import threading
import time

def send_time_request():
    # Terhubung ke server dan mengirim permintaan waktu
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = ('localhost', 45000)
        logging.warning(f"Membuka soket {server_address}")
        sock.connect(server_address)
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] Mengirim {message}")
        sock.sendall(message.encode('utf-8'))
        data = sock.recv(16)
        logging.warning(f"[DITERIMA DARI SERVER] {data}")

if __name__ == '__main__':
    count = 0  # Menginisialisasi penghitung jumlah permintaan
    start_time = time.time()  # Mendapatkan waktu saat ini
    end_time = start_time + 60  # Mengatur waktu berakhir menjadi 1 menit dari waktu mulai

    while time.time() < end_time:
        t = threading.Thread(target=send_time_request)  # Membuat thread baru untuk setiap permintaan
        t.start()  # Memulai thread
        t.join()  # Menunggu thread selesai
        count += 1  # Menambahkan jumlah permintaan

    logging.warning(f"Total pesan request: {count}")  # Mencatat jumlah total permintaan
