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
    start_time = time.time()
    duration = 60  # Durasi waktu dalam detik
    count = 0
    futures = set()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while time.time() - start_time < duration:
            futures.add(executor.submit(send_time_request))
            count += sum(f.done() for f in futures)
            futures = {f for f in futures if not f.done()}

        for future in concurrent.futures.as_completed(futures):
            future.result()

    logging.warning(f"Total pesan request: {count}")
