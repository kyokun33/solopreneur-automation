import subprocess
import time
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = sys.argv[1] if len(sys.argv) > 1 else "https://notebooklm.google.com/"
print(f"🚀 [GUI Direct Shell Launch] 대표님의 실세계 Chrome으로 독립 새 창 전면 팝업: {url}")

# Launch directly using cmd start command to inherit main user GUI session
subprocess.run(f'cmd.exe /c start chrome.exe --new-window "{url}"', shell=True)

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
                print(f"✅ Found GUI Window: '{title}' (HWND {hwnd})")
                force_foreground(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
