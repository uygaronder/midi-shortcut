# mouse_listener.py
import ctypes
from ctypes import wintypes
import sys
from modules.raw_input_common import (MAKEINTRESOURCE, WNDCLASS, RAWINPUTHEADER, RAWMOUSE, RAWINPUT,
                              RAWINPUTDEVICE, WM_INPUT, RIDI_DEVICENAME, RID_INPUT, RIM_TYPEMOUSE,
                              RI_MOUSE_LEFT_BUTTON_DOWN, RI_MOUSE_RIGHT_BUTTON_DOWN, RI_MOUSE_MIDDLE_BUTTON_DOWN,
                              WPARAM, LPARAM, LRESULT, user32, kernel32)

from socketio_instance import socketio  # Ensure socketio is properly initialized

def get_device_name(hDevice):
    size = wintypes.UINT(0)
    if user32.GetRawInputDeviceInfoW(hDevice, RIDI_DEVICENAME, None, ctypes.byref(size)) == -1:
        return None
    buffer = ctypes.create_unicode_buffer(size.value)
    if user32.GetRawInputDeviceInfoW(hDevice, RIDI_DEVICENAME, buffer, ctypes.byref(size)) < 0:
        return None
    return buffer.value

# Define a window procedure for mouse events.
@ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, WPARAM, LPARAM)
def mouse_wndproc(hWnd, msg, wParam, lParam):
    if msg == WM_INPUT:
        dataSize = wintypes.UINT(0)
        if user32.GetRawInputData(lParam, RID_INPUT, None, ctypes.byref(dataSize), ctypes.sizeof(RAWINPUTHEADER)) == -1:
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        # Print data size for debugging.
        # print("Mouse listener: Data size reported:", dataSize.value)
        buffer = ctypes.create_string_buffer(dataSize.value)
        if user32.GetRawInputData(lParam, RID_INPUT, buffer, ctypes.byref(dataSize), ctypes.sizeof(RAWINPUTHEADER)) == -1:
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        # Parse RAWINPUT.
        raw = RAWINPUT.from_buffer_copy(buffer)
        if raw.header.dwType == RIM_TYPEMOUSE:
            buttonFlags = raw.u.mouse.usButtonFlags
            # Only process if a button is pressed.
            if (buttonFlags & RI_MOUSE_LEFT_BUTTON_DOWN) or \
               (buttonFlags & RI_MOUSE_RIGHT_BUTTON_DOWN) or \
               (buttonFlags & RI_MOUSE_MIDDLE_BUTTON_DOWN):
                device_name = get_device_name(raw.header.hDevice)
                data = {"type": "mouse", "device": device_name, "buttonFlags": buttonFlags}
                print("Mouse event:", data)
                if socketio:
                    socketio.emit("raw_input_event", data)
    return user32.DefWindowProcW(hWnd, msg, wParam, lParam)

def create_mouse_window():
    hInstance = kernel32.GetModuleHandleW(None)
    wndclass = WNDCLASS()
    wndclass.style = 0
    wndclass.lpfnWndProc = mouse_wndproc
    wndclass.cbClsExtra = 0
    wndclass.cbWndExtra = 0
    wndclass.hInstance = hInstance
    wndclass.hIcon = user32.LoadIconW(None, MAKEINTRESOURCE(32516))  # IDI_APPLICATION
    wndclass.hCursor = user32.LoadCursorW(None, MAKEINTRESOURCE(32512))  # IDC_ARROW
    wndclass.hbrBackground = user32.GetSysColorBrush(5)  # COLOR_WINDOW
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = "MouseRawInputListener"
    
    if not user32.RegisterClassW(ctypes.byref(wndclass)):
        err = kernel32.GetLastError()
        print("Failed to register mouse window class, error code:", err)
        sys.exit(1)
    
    hWnd = user32.CreateWindowExW(
        0,
        wndclass.lpszClassName,
        "Mouse Raw Input Listener",
        0,
        0, 0, 0, 0,
        None, None,
        hInstance,
        None
    )
    if not hWnd:
        print("Failed to create mouse window")
        sys.exit(1)
    return hWnd

def register_mouse_raw_input(hWnd):
    rid_mouse = RAWINPUTDEVICE()
    rid_mouse.usUsagePage = 0x01
    rid_mouse.usUsage = 0x02  # Mouse
    rid_mouse.dwFlags = 0x00000100  # RIDEV_INPUTSINK
    rid_mouse.hwndTarget = hWnd

    if not user32.RegisterRawInputDevices(ctypes.byref(rid_mouse), 1, ctypes.sizeof(RAWINPUTDEVICE)):
        print("Failed to register mouse raw input device")
        sys.exit(1)

def mouse_listener():
    hWnd = create_mouse_window()
    register_mouse_raw_input(hWnd)
    print("Mouse listener: Listening for raw mouse input... (Press mouse buttons)")
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

if __name__ == "__main__":
    mouse_listener()