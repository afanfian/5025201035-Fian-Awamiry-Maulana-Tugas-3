import socket
import logging
import concurrent.futures
import time

def send_time_request():
    # Membuka socket untuk koneksi ke server dan mengirim permintaan waktu
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = ('localhost', 45000)
        logging.warning(f"Opening socket {server_address}")
        sock.connect(server_address)
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] Sending {message}")
        sock.sendall(message.encode('utf-8'))
        data = sock.recv(16)
        logging.warning(f"[DITERIMA DARI SERVER] {data}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)  # Mengatur level logging
    futures = []
    # Membuka ThreadPoolExecutor yang akan mengelola thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        start_time = time.time()
        while time.time() - start_time < 60:  # Menjalankan selama 1 menit
            # Menyerahkan tugas "send_time_request" ke executor untuk dieksekusi oleh thread
            future = executor.submit(send_time_request)
            futures.append(future)
    # Menunggu semua hasil future selesai sebelum melanjutkan eksekusi
    for future in futures:
        future.result()
    # Mencetak jumlah total pesan request yang telah dikirim
    logging.warning(f"Total pesan request: {len(futures)}")
