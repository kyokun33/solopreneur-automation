import subprocess
import time
import os
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://notebooklm.google.com/"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print(f"🚀 [새 크롬 창 강제 생성] --new-window 스위치로 독립 브라우저 창 띄우기: {url}")

# Run chrome.exe with --new-window to force a new foreground window instead of merging into existing tabs
cmd = [chrome_path, "--new-window", url]
subprocess.Popen(cmd)

time.sleep(1.5)

user32 = ctypes.windll.user32
user32.AllowSetForegroundWindow(-1)

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
                print(f"✅ Found New Chrome Window: {title} (HWND {hwnd})")
                force_foreground(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
