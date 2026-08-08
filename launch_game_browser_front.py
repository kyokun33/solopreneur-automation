import subprocess
import time
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:3000/rogue_project/index.html"
print(f"🚀 [고감독 라이브 브라우저 표출] Chrome 브라우저 형식으로 게임 최상단 구동 중: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [chrome_path, "--new-window", url]
subprocess.Popen(cmd)

time.sleep(1.5)

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
            if "GogoFlex Rogue Project" in title or "Chrome" in title:
                print(f"✅ Found Game Browser Window: {title}")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
