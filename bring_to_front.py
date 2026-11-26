import ctypes

user32 = ctypes.windll.user32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
GetWindowTextW = user32.GetWindowTextW
IsWindowVisible = user32.IsWindowVisible
SetForegroundWindow = user32.SetForegroundWindow
SetWindowPos = user32.SetWindowPos
ShowWindow = user32.ShowWindow

def foreach_window(hwnd, lParam):
    length = GetWindowTextW(hwnd, None, 0)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buff, length + 1)
    title = buff.value
    if IsWindowVisible(hwnd) and any(w in title.lower() for w in ['unity', 'chrome', 'hub', 'rogue']):
        print(f"🚀 Bringing to front: {title} (HWND: {hwnd})")
        ShowWindow(hwnd, 9) # SW_RESTORE
        SetForegroundWindow(hwnd)
        # Position at (0,0) on Display 1
        SetWindowPos(hwnd, -1, 0, 0, 1280, 800, 0x0040)
    return True

if __name__ == "__main__":
    EnumWindows(EnumWindowsProc(foreach_window), 0)
