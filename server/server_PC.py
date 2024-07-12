import socket
import threading
udp_port = 5005
tcp_port = 5006

def get_my_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def udp_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Allow the socket to broadcast
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Bind the socket to all IP addresses on the machine and a specific port
    server_socket.bind(("", 5005))
    
    print("Server is listening...")
    
    while True:
        # Wait for a broadcast message
        message, address = server_socket.recvfrom(1024)
        print(f"Received message from {address}: {message.decode()}")
        
        if message.decode() == "DISCOVER_SERVER":
            response_message = str(tcp_port)
            server_socket.sendto(response_message.encode(), address)
            print(f"Sent server IP response to {address}")

def tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        # Receive data from client
        data = client_socket.recv(1024).decode()
        print(f"Received from {client_address}: {data}")

        # Send data to client
        response = f"{data}"
        client_socket.send(response.encode())

        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_server)
    tcp_thread = threading.Thread(target=tcp_server, args=(get_my_ip(), tcp_port))

    udp_thread.start()
    tcp_thread.start()

    udp_thread.join()
    tcp_thread.join()

