import ctypes
import sys

sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
IsWindowVisible = user32.IsWindowVisible

windows = []

def enum_cb(hwnd, lparam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            title = buff.value
            windows.append((hwnd, title))
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)

print(f"=== [OS 실측 검증] 현재 대표님 모니터에 감지된 모든 가시 윈도우 (총 {len(windows)}개) ===")
for hwnd, title in windows:
    if any(kw in title for kw in ["NotebookLM", "Chrome", "Edge", "GogoFlex", "Antigravity", "1인기업"]):
        print(f"🎯 HWND: {hwnd} | 타이틀: '{title}'")
