import ctypes
import sys

sys.stdout.reconfigure(encoding="utf-8")

user32 = ctypes.windll.user32

def enum_cb(hwnd, extra):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if len(title.strip()) > 0:
                print(f"HWND: {hwnd} | Title: '{title}'")
    return True

CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
user32.EnumWindows(CMPFUNC(enum_cb), 0)
