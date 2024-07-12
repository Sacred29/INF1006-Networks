import socket
server = ""
port = ""

def broadcast_client_udp():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Allow the socket to broadcast
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    broadcast_address = ("<broadcast>", 5005)
    
    # Send broadcast message
    message = "DISCOVER_SERVER"
    client_socket.sendto(message.encode(), broadcast_address)
    print("Broadcast message sent.")
    
    # Wait for response from server
    client_socket.settimeout(5)
    try:
        
        response,  server_address = client_socket.recvfrom(1024)
        global tcp_server_address, tcp_server_port
        tcp_server_address = server_address[0]
        tcp_server_port = response.decode()
        print(f"Received response from {server_address}: {response.decode()}")
    except socket.timeout:
        print("No response from server.")
    
    client_socket.close()

def tcp_client(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Send data to server
    client_socket.send(message.encode())
    
    # Receive data from server
    response = client_socket.recv(1024).decode()
    print(f"{response}")
    
    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    broadcast_client_udp()
    if tcp_server_address is not None and tcp_server_port is not None:
        tcp_client(tcp_server_address, int(tcp_server_port), "TCP 3-Way Handshake Established!")
        


