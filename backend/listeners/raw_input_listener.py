import ctypes
from ctypes import wintypes
import sys

from socketio_instance import socketio  # Ensure this is initialized in your main app

# Helper: Convert an integer to a resource pointer.
def MAKEINTRESOURCE(i):
    return ctypes.cast(ctypes.c_void_p(i), wintypes.LPCWSTR)

# Define missing handle types if not present.
if not hasattr(wintypes, 'HCURSOR'):
    wintypes.HCURSOR = wintypes.HANDLE
if not hasattr(wintypes, 'HICON'):
    wintypes.HICON = wintypes.HANDLE
if not hasattr(wintypes, 'HBRUSH'):
    wintypes.HBRUSH = wintypes.HANDLE

# Define WPARAM and LPARAM for 64-bit compatibility.
if ctypes.sizeof(ctypes.c_void_p) == 8:
    WPARAM = ctypes.c_ulonglong
    LPARAM = ctypes.c_longlong
else:
    WPARAM = ctypes.c_ulong
    LPARAM = ctypes.c_long

if hasattr(wintypes, 'LRESULT'):
    LRESULT = wintypes.LRESULT
else:
    LRESULT = ctypes.c_long

# Constants for raw input.
WM_INPUT = 0x00FF
RIDI_DEVICENAME = 0x20000007
RID_INPUT = 0x10000003
RIM_TYPEKEYBOARD = 1

# --- Structure Definitions (using default alignment) ---

class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, WPARAM, LPARAM)),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM)
    ]

class RAWKEYBOARD(ctypes.Structure):
    _fields_ = [
        ("MakeCode", wintypes.USHORT),
        ("Flags", wintypes.USHORT),
        ("Reserved", wintypes.USHORT),
        ("VKey", wintypes.USHORT),
        ("Message", wintypes.UINT),
        ("ExtraInformation", wintypes.ULONG)
    ]

class RAWINPUT_U(ctypes.Union):
    _fields_ = [
        ("keyboard", RAWKEYBOARD),
        # We omit mouse fields.
    ]

class RAWINPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("u", RAWINPUT_U)
    ]

class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT),
        ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND)
    ]

# --- End Structures ---

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Set argument types for DefWindowProcW.
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, WPARAM, LPARAM]
user32.DefWindowProcW.restype = LRESULT

def get_device_name(hDevice):
    size = wintypes.UINT(0)
    if user32.GetRawInputDeviceInfoW(hDevice, RIDI_DEVICENAME, None, ctypes.byref(size)) == -1:
        return None
    buffer = ctypes.create_unicode_buffer(size.value)
    if user32.GetRawInputDeviceInfoW(hDevice, RIDI_DEVICENAME, buffer, ctypes.byref(size)) < 0:
        return None
    return buffer.value

@ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, WPARAM, LPARAM)
def wndproc(hWnd, msg, wParam, lParam):
    if msg == WM_INPUT:
        dataSize = wintypes.UINT(0)
        if user32.GetRawInputData(lParam, RID_INPUT, None, ctypes.byref(dataSize), ctypes.sizeof(RAWINPUTHEADER)) == -1:
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        buffer = ctypes.create_string_buffer(dataSize.value)
        if user32.GetRawInputData(lParam, RID_INPUT, buffer, ctypes.byref(dataSize), ctypes.sizeof(RAWINPUTHEADER)) == -1:
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        try:
            raw = RAWINPUT.from_buffer_copy(buffer)
        except Exception as e:
            print("Error copying buffer:", e)
            return user32.DefWindowProcW(hWnd, msg, wParam, lParam)
        
        # Process only keyboard events.
        if raw.header.dwType == RIM_TYPEKEYBOARD:
            device_name = get_device_name(raw.header.hDevice)
            vkey = raw.keyboard.VKey
            key_message = raw.keyboard.Message
            data = {"type": "keyboard", "device": device_name, "vkey": vkey, "message": key_message}
            #print("Keyboard event:", data)
            if socketio:
                socketio.emit("raw_input_event", data)
    return user32.DefWindowProcW(hWnd, msg, wParam, lParam)

def create_message_window():
    hInstance = kernel32.GetModuleHandleW(None)
    wndclass = WNDCLASS()
    wndclass.style = 0
    wndclass.lpfnWndProc = wndproc
    wndclass.cbClsExtra = 0
    wndclass.cbWndExtra = 0
    wndclass.hInstance = hInstance
    wndclass.hIcon = user32.LoadIconW(None, MAKEINTRESOURCE(32516))  # IDI_APPLICATION
    wndclass.hCursor = user32.LoadCursorW(None, MAKEINTRESOURCE(32512))  # IDC_ARROW
    wndclass.hbrBackground = user32.GetSysColorBrush(5)  # COLOR_WINDOW
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = "RawInputListener"
    
    if not user32.RegisterClassW(ctypes.byref(wndclass)):
        err = kernel32.GetLastError()
        print("Failed to register window class, error code:", err)
        sys.exit(1)
    
    hWnd = user32.CreateWindowExW(
        0,
        wndclass.lpszClassName,
        "Raw Input Listener",
        0,
        0, 0, 0, 0,
        None, None,
        hInstance,
        None
    )
    if not hWnd:
        print("Failed to create window")
        sys.exit(1)
    return hWnd

def register_raw_input(hWnd):
    # Create a RAWINPUTDEVICE for keyboard only.
    rid = RAWINPUTDEVICE()
    rid.usUsagePage = 0x01  # Generic desktop controls
    rid.usUsage = 0x06      # Keyboard
    rid.dwFlags = 0x00000100  # RIDEV_INPUTSINK: Receive input even when not in focus.
    rid.hwndTarget = hWnd
    if not user32.RegisterRawInputDevices(ctypes.byref(rid), 1, ctypes.sizeof(rid)):
        print("Failed to register raw input devices")
        sys.exit(1)

def main():
    hWnd = create_message_window()
    register_raw_input(hWnd)
    print("Listening for raw keyboard input... (Press keys to see events)")
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

if __name__ == "__main__":
    main()
