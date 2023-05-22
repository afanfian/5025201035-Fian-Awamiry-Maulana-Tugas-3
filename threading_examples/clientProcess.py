import socket
import logging
import multiprocessing
import time

def send_time_request():
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
    duration = 60  # Durasi waktu dalam 60 detik
    start_time = time.time()  # Waktu awal sebelum memulai loop
    process_count = 0  # Counter untuk jumlah proses yang dibuat

    while time.time() - start_time < duration:
        p = multiprocessing.Process(target=send_time_request)
        p.start()
        p.join()
        process_count += 1

    logging.warning(f"Total pesan request: {process_count}")
