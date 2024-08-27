from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    audioVolume = cast(interface, POINTER(IAudioEndpointVolume))
    audioVolume.SetMasterVolumeLevelScalar(float(volume) / 127, None)

def open_app(app_name):
    app_map = {
        "spotify": "spotify",
        "chrome": "chrome",
        "notepad": "notepad"
    }
    pyautogui.press("win")
    pyautogui.typewrite(app_map[app_name])
    pyautogui.press("enter")

"""
def simulateKeyPress(key):
    pyautogui.press(key)

def simulate_system_action(action):
    action_map = {
        "volume_up": "volumeup",
        "volume_down": "volumedown",
        "mute": "volumemute"
    }
    simulateKeyPress(action_map[action])
"""