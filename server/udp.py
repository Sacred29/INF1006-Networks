import socket
import time

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def broadcast_ip():
    server_ip = get_private_ip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        message = f'SERVER_IP:{server_ip}'
        sock.sendto(message.encode(), ('<broadcast>', 37020))
        print(f"Broadcasting IP address: {server_ip}")
        attempts += 1
        time.sleep(5)

    print("Broadcasting stopped")

if __name__ == '__main__':
    broadcast_ip()
