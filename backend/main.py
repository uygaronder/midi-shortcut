from modules.midi_handler import midi_listener
from modules.data_manager import load_data, save_data

file_path = "storage/shortcuts.json"
loaded_data = load_data(file_path)

def menu():
    print("1. Listen to MIDI")
    choice = input("Enter choice: ")
    if choice == "1":
        midi_listener(loaded_data)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    #menu()
    midi_listener(loaded_data)
