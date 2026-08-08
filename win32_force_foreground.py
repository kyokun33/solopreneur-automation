import ctypes
import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Allow any process to set foreground window
user32.AllowSetForegroundWindow(-1)

def force_foreground(hwnd):
    # Restore window if minimized
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    
    # Simulate ALT key to bypass Windows SetForegroundWindow lock
    user32.keybd_event(0x12, 0, 0, 0) # ALT down
    user32.keybd_event(0x12, 0, 2, 0) # ALT up
    
    foreground_hwnd = user32.GetForegroundWindow()
    if foreground_hwnd != hwnd:
        foreground_thread_id = user32.GetWindowThreadProcessId(foreground_hwnd, None)
        target_thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        
        user32.AttachThreadInput(foreground_thread_id, target_thread_id, True)
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)
        user32.AttachThreadInput(foreground_thread_id, target_thread_id, False)
    else:
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)

print("🚀 [Win32 Foreground Lock Bypassed] 대표님 모니터 전면에 브라우저/계산기 창 100% 강제 표출 중...")

# Launch Chrome with game URL via explorer.exe to inherit Interactive Shell session
url = "http://localhost:3000/rogue_project/index.html"
subprocess.Popen(["explorer.exe", url])
time.sleep(1.5)

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
            if "GogoFlex Rogue Project" in title or "Chrome" in title or "localhost" in title:
                print(f"✅ Found Target Window: {title} (HWND {hwnd})")
                force_foreground(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
