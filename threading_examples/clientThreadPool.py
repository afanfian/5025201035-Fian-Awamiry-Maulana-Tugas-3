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
    start_time = time.time()  # Menyimpan waktu awal
    duration = 60  # Durasi waktu dalam 60 detik
    count = 0  # Jumlah pesan request
    futures = set()  # Set untuk menyimpan objek future

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while time.time() - start_time < duration:
            # Mengirimkan tugas "send_time_request" ke executor untuk dieksekusi oleh thread
            futures.add(executor.submit(send_time_request))
            # Menghitung jumlah future yang telah selesai
            count += sum(f.done() for f in futures)
            # Menghapus future yang telah selesai dari set
            futures = {f for f in futures if not f.done()}

        for future in concurrent.futures.as_completed(futures):
            future.result()  # Menunggu hasil future selesai

    logging.warning(f"Total pesan request: {count}")  # Menampilkan jumlah total pesan request yang telah dikirim
