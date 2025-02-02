# backend/endpoints/devices.py
from flask import Blueprint, jsonify, request
from utils.device_utils import get_midi_devices, get_keyboard_devices, get_other_devices
from modules.data_manager import load_configs, save_configs

devices_bp = Blueprint('devices', __name__)

def construct_device_id(device_type, device_name):
    """Create a unique device ID from the type and name (spaces removed)."""
    return f"{device_type}_{device_name.replace(' ', '')}"

@devices_bp.route('/', methods=['GET'])
def list_devices():
    # Get discovered devices.
    discovered = {
        "midi": get_midi_devices(),
        "keyboard": get_keyboard_devices(),
        "other": get_other_devices()
    }
    
    # Load saved configurations.
    configs = load_configs()
    # Create a dictionary keyed by device_id for quick lookup.
    config_dict = {}
    for config in configs:
        device = config.get("device")
        if device:
            device_id = construct_device_id(device.get("type", ""), device.get("name", ""))
            config_dict[device_id] = config

    # For each discovered device, check if it exists in saved configs.
    # We'll create a merged result that for each type is a list of objects with both
    # the discovered device name and an optional configuration.
    merged = {}
    for device_type, device_list in discovered.items():
        merged[device_type] = []
        for device_name in device_list:
            device_id = construct_device_id(device_type, device_name)
            # If no config exists for this device, log it and create a default config entry.
            if device_id not in config_dict:
                # Create a default configuration. You can later allow the user to customize these.
                default_logos = {
                    "midi": "piano",
                    "keyboard": "keyboard",
                    "other": "device"
                }
                default_config = {
                    "device": {
                        "type": device_type,
                        "name": device_name
                    },
                    "config": {
                        "displayName": device_name,
                        "logo": default_logos.get(device_type, ""),  # set default logo URL based on type
                        "color": "#ffffff",  # default color white (or any color)
                        "shortcuts": {}  # initially empty shortcuts
                    }
                }
                # Optionally, log this new device configuration for future reference.
                print(f"New device discovered (no config found): {device_id}. Creating default config.")
                # Add it to the lookup and optionally to the list of configurations.
                config_dict[device_id] = default_config
                configs.append(default_config)
                # Save the updated configurations for future use.
                save_configs(configs)
            # Add the merged result.
            merged[device_type].append({
                "name": device_name,
                "config": config_dict[device_id]["config"]
            })
    
    # Return the merged result.
    return jsonify(merged)

# Other endpoints for individual configuration retrieval and updates remain unchanged:
@devices_bp.route('/device-configs', methods=['GET'])
def list_device_configs():
    configs = load_configs()
    return jsonify(configs)

@devices_bp.route('/device-configs/<device_id>', methods=['GET'])
def get_device_config(device_id):
    configs = load_configs()
    for config in configs:
        device = config.get("device")
        if device:
            cfg_id = construct_device_id(device.get("type", ""), device.get("name", ""))
            if cfg_id == device_id:
                return jsonify(config)
    return jsonify({"error": "Device config not found"}), 404

@devices_bp.route('/device-configs', methods=['POST'])
def create_device_configs():
    new_configs = request.get_json()
    if not isinstance(new_configs, list):
        return jsonify({"error": "Expected a list of configurations"}), 400
    try:
        save_configs(new_configs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"status": "success", "configs": new_configs}), 200

@devices_bp.route('/device-configs/<device_id>', methods=['POST'])
def create_device_config(device_id):
    new_config = request.get_json()
    if not new_config or "device" not in new_config:
        return jsonify({"error": "Invalid configuration data"}), 400

    configs = load_configs()
    updated = False
    new_config_id = construct_device_id(new_config["device"].get("type", ""), new_config["device"].get("name", ""))

    for idx, config in enumerate(configs):
        device = config.get("device")
        if device:
            cfg_id = construct_device_id(device.get("type", ""), device.get("name", ""))
            if cfg_id == new_config_id:
                configs[idx] = new_config
                updated = True
                break

    if not updated:
        configs.append(new_config)

    try:
        save_configs(configs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "config": new_config}), 200
