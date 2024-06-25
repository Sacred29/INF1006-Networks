import requests
import socketio
import threading
import socket

server_ip = None

def listen_for_server_ip():
    global server_ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", 37020))

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        if message.startswith("SERVER_IP:"):
            server_ip = message.split(":")[1]
            print(f"Discovered server IP: {server_ip}")
            return server_ip

# Run the UDP listener in a separate thread
ip_thread = threading.Thread(target=listen_for_server_ip)
ip_thread.start()
ip_thread.join()

# HTTP client code to interact with the HTTP endpoints
def send_http_message(server_ip, message):
    url = f'http://{server_ip}:5000/api/message'
    response = requests.post(url, json={'message': message})
    print(f"HTTP response: {response.json()}")

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")
    sio.send("Client connected via WebSocket")

@sio.event
def message(data):
    print(f"Received message: {data}")

@sio.event
def disconnect():
    print("Disconnected from the server")

if __name__ == '__main__':
    if server_ip:
        sio.connect(f'http://{server_ip}:5000', transports=['websocket'])
        sio.wait()

        # Example of sending a message to the HTTP endpoint
        send_http_message(server_ip, "Hello from HTTP client")
