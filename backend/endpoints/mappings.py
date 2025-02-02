# modules/data_manager.py
import json
import os

# Determine the base directory for storing files.
# You can change this to another folder if desired.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, 'storage')

# Ensure the storage directory exists.
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# Define the full path to the JSON configuration file.
CONFIG_FILE_PATH = os.path.join(STORAGE_DIR, 'device_configs.json')

def load_configs():
    """Load device configuration from a JSON file.
    
    Returns:
        A list of configuration objects. If the file does not exist, returns an empty list.
    """
    if not os.path.exists(CONFIG_FILE_PATH):
        return []  # No configurations saved yet.
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            configs = json.load(f)
        return configs
    except Exception as e:
        print("Error loading configurations:", e)
        return []

def save_configs(configs):
    """Save the device configuration to a JSON file.
    
    Args:
        configs: A list of configuration objects.
    """
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(configs, f, indent=2)
    except Exception as e:
        print("Error saving configurations:", e)
