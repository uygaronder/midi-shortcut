from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import pyautogui
import os
import webbrowser

def accept_input(msg, input):
    if input["type"] == "control_change" and input["control"] == msg.control:
        if input["output"]["type"]=="volume":
            adjust_volume(msg.value, input["output"]["params"]["app"])
    elif input["type"] == "note_on" and input["note"] == msg.note:
        if input["output"]["type"]=="open_app":
            open_app(input["output"]["params"]["app"])
        elif input["output"]["type"]=="open_web_page":
            open_web_page(input["output"]["params"]["url"])

def adjust_volume(value, app='master'):
    volume_percentage = value / 127
    if app == 'master':
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        audioVolume = cast(interface, POINTER(IAudioEndpointVolume))
        audioVolume.SetMasterVolumeLevelScalar(volume_percentage, None)
    else:
        sessions = AudioUtilities.GetAllSessions()
        app_name = app.lower()
        for session in sessions:
            process = session.Process
            if process and process.name().lower() == app_name:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume.SetMasterVolume(volume_percentage, None)
                return
        print(f"Application {app_name} not found.")

def open_app(app_name):
    os.system(f"start {app_name}")
    pass

def open_web_page(url):
    webbrowser.open(url)
    pass

def open_in_incognito(url):
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito").open(url)

def open_file(file_path):
    os.system(f"start {file_path}")

def toggle_mute():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    audioVolume = cast(interface, POINTER(IAudioEndpointVolume))
    audioVolume.SetMute(not audioVolume.GetMute(), None)

def toggle_microphone_mute():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    audioVolume = cast(interface, POINTER(IAudioEndpointVolume))
    audioVolume.SetMute(not audioVolume.GetMute(), None)

"""
data example: 

{
    "devices": [
        {
            "name": "Launchkey Mini 0",
            "type": "midi",
            "inputs": [
                {
                    "type": "note_on",
                    "channel": 9,
                    "note": 40,
                    "output": {
                        "type": "open_web_page",
                        "params": {
                            "app": "chrome.exe",
                            "url": "https://www.notion.so"
                        }    
                    }
                },
                {
                    "type": "note_on",
                    "channel": 9,
                    "note": 41,
                    "output": {
                        "type": "open_app",
                        "params": {
                            "app": "notepad",
                            "path": ["C:\\Users\\user\\Desktop\\test.txt"]
                        }    
                    }
                },
                {
                    "type": "control_change",
                    "channel": 0,
                    "control": 21,
                    "output": {
                        "type": "volume",
                        "params": {
                            "app": "master"
                        }    
                    }
                },
                {
                    "type": "control_change",
                    "channel": 0,
                    "control": 22,
                    "output": {
                        "type": "volume",
                        "params": {
                            "app": "spotify.exe"
                        }    
                    }
                },
                {
                    "type": "control_change",
                    "channel": 0,
                    "control": 23,
                    "output": {
                        "type": "volume",
                        "params": {
                            "app": "chrome.exe"
                        }    
                    }
                }
            ]
        }
    ]
}    




"""