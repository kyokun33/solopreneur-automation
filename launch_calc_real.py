import subprocess
import time
import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 [UWP Shell COM Activation] 대표님 모니터 전면에 진짜 계산기 창 띄우기 구동 중...")

# ShellExecute via PowerShell COM object
cmd = 'powershell -Command "$s = New-Object -ComObject Shell.Application; $s.ShellExecute(\'calc.exe\', \'\', \'\', \'open\', 1)"'
subprocess.run(cmd, shell=True)

time.sleep(1.5)

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
            if "계산기" in title or "Calculator" in title:
                print(f"🎉 [성공!] 계산기 UI 윈도우 감지됨: {title} (HWND {hwnd})")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
