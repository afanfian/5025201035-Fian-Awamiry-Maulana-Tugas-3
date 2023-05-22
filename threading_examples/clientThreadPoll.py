import socket
import logging
import concurrent.futures
import threading

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
    logging.basicConfig(level=logging.WARNING)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        i = 0
        while i < 20:
            future = executor.submit(send_time_request)
            futures.append(future)
            i += 1
        
        # Tunggu semua task selesai
        concurrent.futures.wait(futures)
    thread_count = threading.active_count()
    logging.warning(f"Jumlah thread: {thread_count}")