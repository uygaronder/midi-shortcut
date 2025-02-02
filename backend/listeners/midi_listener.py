import mido
import time
from socketio_instance import socketio  # Ensure this is initialized

def midi_listener():
    try:
        # List available input ports for debugging:
        ports = mido.get_input_names()
        print("Available MIDI input ports:", ports)
        
        # Open the first available MIDI input port.
        # In a real application, you might allow the user to select a port.
        with mido.open_input(ports[0]) as inport:
            print(f"Listening for MIDI messages on {inport.name}...")
            while True:
                for msg in inport.iter_pending():
                    # Convert the MIDI message to a dictionary.
                    data = {"type": "midi", "message": msg.dict(), "device": inport.name}
                    #print("MIDI event:", data)
                    if socketio:
                        socketio.emit("raw_input_event", data)
                time.sleep(0.01)  # Polling delay
    except Exception as e:
        print("Error in MIDI listener:", e)

if __name__ == "__main__":
    print("Starting MIDI listener...")
    midi_listener()