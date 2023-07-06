from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
# Create a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# Enable CORS for all origins
CORS(app)

orders = [
    {'id': 1,"item":"chana", 'status': 'Pending'},
    {'id': 2,"item":"samosa", 'status': 'Progress'},
    {'id': 3,"item":"paranta", 'status': 'Completed'}
]
# Initialize the Socket.IO extension
socketio = SocketIO(app)

# Define a route for the home page
@app.route('/')
def index():
    
    return jsonify(orders)


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    new_status = request.json.get('status')
    for order in orders:
        if order['id'] == order_id:
            order['status'] = new_status
            # Emit an event to notify clients about the status change
            socketio.emit('order_status_changed', {'id': order_id, 'status': new_status})
            break
    return jsonify({'message': 'Order status updated'})


# Define an event handler for the 'connect' event
@socketio.on('connect')
def connect():
    print('Client connected')

# Define an event handler for the 'message' event
@socketio.on('message')
def message(data):
    print('Received message:', data)
    emit('response', 'Server received your message')

# Define an event handler for the 'disconnect' event
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Run the Flask application with Socket.IO support
    socketio.run(app, host='localhost', port=8000)