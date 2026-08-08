import subprocess
import time
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32
user32.AllowSetForegroundWindow(-1)

print("🚀 [Win32 GUI 테스트] 클래식 Win32 GUI 메모장(notepad.exe) 띄우기 테스트...")

proc = subprocess.Popen(["notepad.exe"])
time.sleep(1)

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
IsWindowVisible = user32.IsWindowVisible

def enum_cb(hwnd, lparam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            title = buff.value
            if "메모장" in title or "Notepad" in title:
                print(f"✅ Found Notepad Window: {title} (HWND {hwnd})")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
