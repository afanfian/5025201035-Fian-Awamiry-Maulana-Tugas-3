import socket
import logging
import threading
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
    thread_count = 0
    start_time = time.time()
    end_time = start_time + 60  # Waktu berjalan selama 1 menit

    while time.time() < end_time:
        t = threading.Thread(target=send_time_request)
        t.start()
        t.join()
        thread_count += 1

    logging.warning(f"Jumlah thread: {thread_count}")
