import socket
import logging
import concurrent.futures
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
    request_count = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(60):
            future = executor.submit(send_time_request)
            future.result()
            request_count += 1

    logging.warning(f"Total pesan request: {request_count}")
