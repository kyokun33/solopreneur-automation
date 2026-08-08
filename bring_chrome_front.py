import ctypes

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
            if "Chrome" in title or "Google" in title or "NotebookLM" in title or "로그인" in title:
                print(f"Found Window: {title}")
                user32.ShowWindow(hwnd, 9)
                user32.SetForegroundWindow(hwnd)
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)
