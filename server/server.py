from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from udp import broadcast_ip
import threading
from client_PC import broadcast_client_udp
app = Flask(__name__)
socketio = SocketIO(app)

clients = {}

def find_sid(ip):
    for sid in clients:
        if clients[sid] == ip:
            return sid
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/broadcast')
def broadcast():
	broadcast_ip()
	return "broadcast ended"

@app.route('/clients')
def get_clients():
	return jsonify(list(clients.values()))

@app.route('/unicast', methods=['POST'])
def unicast():
    data = request.get_json()
    target_ip = data.get('ip')
    message = data.get('message')
    print(f"target_ip : {target_ip}")
    print(f"clients: {clients}")
    if target_ip in clients.values():
        print("SUCCESS")
        target_sid = find_sid(target_ip)
        socketio.send(message, to=target_sid)
        
        return jsonify({'status': 'success', 'message': f"message sent to {target_ip}"}), 200
    else:
        return jsonify({'status': 'error', 'message': f"Client {target_ip} not connected"}), 404

@app.route('/api/message', methods=['POST'])
def api_message():
    data = request.json
    message = data.get('message')
    if message:
        # Broadcast the message to all connected WebSocket clients
        socketio.emit('message', message)
        return jsonify({"status": "Message sent"}), 200
    else:
        return jsonify({"error": "No message provided"}), 400

@socketio.on('connect')
def handle_connect():
    client_ip = request.remote_addr
    client_id = request.sid
    clients[client_id] = client_ip
    print('Client connected')
    send('Welcome to the WebSocket server!')

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Echo: {msg}")

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in clients:
        client_ip = clients.pop(client_id)
        print(f"client disconnected: {client_ip} (ID: {client_id})")
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

