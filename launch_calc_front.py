import subprocess
import time
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Windows 계산기 실행 및 화면 최상단 전면 표출 중...")
subprocess.Popen(["calc.exe"])
time.sleep(1)

user32 = ctypes.windll.user32
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
            if "계산기" in title or "Calculator" in title:
                print(f"✅ Found Calculator Window: {title}")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
