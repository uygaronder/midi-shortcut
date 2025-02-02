# backend/utils/device_utils.py
import mido

import ctypes
from ctypes import wintypes

RIM_TYPEKEYBOARD = 1
RIDI_DEVICENAME = 0x20000007

class RAWINPUTDEVICELIST(ctypes.Structure):
    _fields_ = [
        ("hDevice", wintypes.HANDLE),
        ("dwType", wintypes.DWORD)
    ]

def get_keyboard_devices_pywin32():
    """
    Enumerate keyboard devices using Windows Raw Input API.
    Returns a list of dictionaries with device information.
    """
    user32 = ctypes.windll.user32

    # First, call GetRawInputDeviceList with None to get the number of devices.
    num_devices = wintypes.UINT(0)
    if user32.GetRawInputDeviceList(None, ctypes.byref(num_devices), ctypes.sizeof(RAWINPUTDEVICELIST)) != 0:
        raise ctypes.WinError()

    # Allocate an array for the device list.
    device_array = (RAWINPUTDEVICELIST * num_devices.value)()
    if user32.GetRawInputDeviceList(device_array, ctypes.byref(num_devices), ctypes.sizeof(RAWINPUTDEVICELIST)) == -1:
        raise ctypes.WinError()

    GetRawInputDeviceInfo = user32.GetRawInputDeviceInfoW
    keyboards = []
    
    for device in device_array:
        if device.dwType == RIM_TYPEKEYBOARD:
            # First, get the size of the device name string.
            size = wintypes.UINT(0)
            if GetRawInputDeviceInfo(device.hDevice, RIDI_DEVICENAME, None, ctypes.byref(size)) == -1:
                continue

            # Create a buffer for the device name.
            buffer = ctypes.create_unicode_buffer(size.value)
            if GetRawInputDeviceInfo(device.hDevice, RIDI_DEVICENAME, buffer, ctypes.byref(size)) < 0:
                continue

            device_name = buffer.value

            # Optionally, you could extract additional info (like vendor ID, product ID) if needed.
            keyboards.append(device_name)
    
    return keyboards

def get_midi_devices():
    """Return a list of available MIDI input device names."""
    try:
        return mido.get_input_names()
    except Exception as e:
        print("Error retrieving MIDI devices:", e)
        return []

def get_keyboard_devices():
    """
    Return a list of available keyboard devices.
    
    """
    try:
        keyboards = get_keyboard_devices_pywin32()

        return keyboards
    except Exception as e:
        print("Error retrieving keyboard devices:", e)
        return []

def get_other_devices():
    """
    Return a list of other input devices.
    
    """
    try:
        from inputs import devices
        other_names = []
        
        # Gather mouse device names.
        if hasattr(devices, 'mice'):
            mice = devices.mice
            other_names.extend([m.name for m in mice])
        
        # Gather gamepad device names.
        if hasattr(devices, 'gamepads'):
            gamepads = devices.gamepads
            other_names.extend([g.name for g in gamepads])
        
        return other_names
    except Exception as e:
        print("Error retrieving other devices:", e)
        return []
