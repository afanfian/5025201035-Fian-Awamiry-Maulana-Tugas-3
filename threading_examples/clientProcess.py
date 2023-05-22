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
    # Durasi waktu dalam 60 detik
    duration = 60
    def clientProcess():
        process = multiprocessing.Process(target=send_time_request)
        process.start()
        process.join()
    # Waktu awal sebelum memulai loop
    start_time = time.time()
    # Daftar proses yang dibuat
    processes = []
    while time.time() - start_time < duration:
        # Membuat dan menjalankan proses baru
        process = multiprocessing.Process(target=send_time_request)
        process.start()
        processes.append(process)
    for process in processes:
        # Menunggu proses selesai
        process.join()
    # Jumlah total proses yang dibuat
    count = len(processes)
    logging.warning(f"Total pesan request: {count}")
