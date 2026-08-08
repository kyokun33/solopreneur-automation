import ctypes
import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32
user32.AllowSetForegroundWindow(-1)

url = "https://notebooklm.google.com/"
print(f"🚀 [고감독 라이브 표출] 대표님 디스플레이 1 전면에 NotebookLM 브라우저 띄우는 중: {url}")

subprocess.Popen(["explorer.exe", url])
time.sleep(1.5)

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
IsWindowVisible = user32.IsWindowVisible

def force_foreground(hwnd):
    user32.ShowWindow(hwnd, 9)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)

def enum_cb(hwnd, lparam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            title = buff.value
            if "NotebookLM" in title or "Chrome" in title:
                print(f"✅ Found Target Window: {title} (HWND {hwnd})")
                force_foreground(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
