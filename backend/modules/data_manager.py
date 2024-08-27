import json
import os

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            print(f"Data loaded from {file_path}")
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return {}

def save_data(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
            print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data: {e}")
