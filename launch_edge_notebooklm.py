import subprocess
import time
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://notebooklm.google.com/"
print(f"🚀 [Edge Display Engine] Microsoft Edge 브라우저로 NotebookLM 전면 구동 중: {url}")

subprocess.run(f'start msedge.exe --new-window "{url}"', shell=True)
time.sleep(2.0)

user32 = ctypes.windll.user32
user32.AllowSetForegroundWindow(-1)

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
            if "NotebookLM" in title or "Edge" in title:
                print(f"🎉 [성공!] 브라우저 윈도우 실물 감지됨: '{title}' (HWND {hwnd})")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
