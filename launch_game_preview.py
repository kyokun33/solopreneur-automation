import subprocess
import time
import ctypes
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\rogue_project\index.html")
print(f"🚀 [고감독 실시간 시각화] 로그프로젝트 게임 1단계 알파 빌드 최상단 표출 중: {html_path}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [chrome_path, "--new-window", html_path]
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
                print(f"✅ Found Game Window: {title}")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
