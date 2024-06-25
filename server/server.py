from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from udp import broadcast_ip

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/broadcast')
def broadcast():
	broadcast_ip()
	return "broadcast ended"

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
    print('Client connected')
    send('Welcome to the WebSocket server!')

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Echo: {msg}")

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
