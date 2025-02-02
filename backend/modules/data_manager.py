# modules/data_manager.py
import json
import os

# Define a file path for storing the configuration data.
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'device_configs.json')

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