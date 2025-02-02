from flask import Flask, request, jsonify
from flask_cors import CORS
from endpoints import register_blueprints
import threading

# Import and initialize Flask-SocketIO.
from flask_socketio import SocketIO
from socketio_instance import socketio

def create_app():
    app = Flask(__name__)
    CORS(app)
    register_blueprints(app)

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the MIDI API"})
    return app

if __name__ == "__main__":
    app = create_app()

    # Initialize SocketIO and assign it to the shared module.
    from socketio_instance import socketio  # get the shared variable
    socketio = SocketIO(app, cors_allowed_origins="*")
    import socketio_instance
    socketio_instance.socketio = socketio

    # Emit a test event.
    socketio.emit("raw_input_event", {"device": "test", "vkey": 999, "message": 123})

    # Import the listener functions.
    from listeners.raw_input_listener import main as raw_input_main
    from listeners.midi_listener import midi_listener

    # Start the raw input (keyboard/mouse) listener thread.
    #listener_thread = threading.Thread(target=raw_input_main, daemon=True)
    #listener_thread.start()

    # Start the MIDI listener thread.
    midi_thread = threading.Thread(target=midi_listener, daemon=True)
    midi_thread.start()

    # Use socketio.run instead of app.run to ensure SocketIO works correctly.
    socketio.run(app, host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))
