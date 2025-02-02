# raw_input_common.py
import ctypes
from ctypes import wintypes

# Helper for resource conversion.
def MAKEINTRESOURCE(i):
    return ctypes.cast(ctypes.c_void_p(i), wintypes.LPCWSTR)

# Ensure missing handle types exist.
if not hasattr(wintypes, 'HCURSOR'):
    wintypes.HCURSOR = wintypes.HANDLE
if not hasattr(wintypes, 'HICON'):
    wintypes.HICON = wintypes.HANDLE
if not hasattr(wintypes, 'HBRUSH'):
    wintypes.HBRUSH = wintypes.HANDLE

# WPARAM and LPARAM for 64-bit compatibility.
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

# Constants.
WM_INPUT = 0x00FF
RIDI_DEVICENAME = 0x20000007
RID_INPUT = 0x10000003
RIM_TYPEKEYBOARD = 1
RIM_TYPEMOUSE = 0

# Mouse button down flags.
RI_MOUSE_LEFT_BUTTON_DOWN   = 0x0001
RI_MOUSE_RIGHT_BUTTON_DOWN  = 0x0004
RI_MOUSE_MIDDLE_BUTTON_DOWN = 0x0010

# Structure definitions (using default alignment)
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

# For mouse events we use the standard RAWMOUSE.
class RAWMOUSE(ctypes.Structure):
    _fields_ = [
        ("usFlags", wintypes.USHORT),
        ("usButtonFlags", wintypes.USHORT),
        ("usButtonData", wintypes.USHORT),
        ("ulRawButtons", wintypes.ULONG),
        ("lLastX", ctypes.c_long),
        ("lLastY", ctypes.c_long),
        ("ulExtraInformation", wintypes.ULONG)
    ]

# Define a union that holds both keyboard and mouse.
class RAWINPUT_U(ctypes.Union):
    _fields_ = [
        ("keyboard", RAWKEYBOARD),
        ("mouse", RAWMOUSE)
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

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Set DefWindowProcW argument types.
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, WPARAM, LPARAM]
user32.DefWindowProcW.restype = LRESULT