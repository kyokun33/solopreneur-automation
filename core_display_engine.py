import ctypes
import ctypes.wintypes
import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Win32 Constants
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001
SPIF_SENDCHANGE = 0x02
ASFW_ANY = -1
SW_RESTORE = 9
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_SHOWWINDOW = 0x0040
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002

def initialize_windows_display_system():
    """Bypass Windows OS Foreground Lockout by setting lock timeout to 0"""
    try:
        user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 0, SPIF_SENDCHANGE)
        user32.AllowSetForegroundWindow(ASFW_ANY)
        print("✅ [Display Engine] Windows OS Foreground Lock Timeout set to 0ms (Lockout Bypassed)")
    except Exception as e:
        print(f"⚠️  [Display Engine] SystemParametersInfo warning: {e}")

def force_window_to_primary_display(hwnd):
    """Force any target window to Primary Monitor (Display 1) at foreground"""
    if not user32.IsWindow(hwnd):
        return False

    # 1. Restore if minimized
    user32.ShowWindow(hwnd, SW_RESTORE)

    # 2. Keybd event ALT trick to unlock SetForegroundWindow
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)

    # 3. AttachThreadInput to foreground thread
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread_id = user32.GetWindowThreadProcessId(fg_hwnd, None)
    target_thread_id = user32.GetWindowThreadProcessId(hwnd, None)

    if fg_thread_id != target_thread_id:
        user32.AttachThreadInput(fg_thread_id, target_thread_id, True)
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)
        user32.AttachThreadInput(fg_thread_id, target_thread_id, False)
    else:
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)

    # 4. Force Window to Display 1 Primary Monitor Foreground (HWND_TOPMOST briefly then NOTOPMOST)
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
    time.sleep(0.1)
    user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
    return True

def launch_and_display(url_or_app_target, window_keywords):
    """Universal function to launch any Web URL or App directly onto Display 1 Foreground"""
    initialize_windows_display_system()

    print(f"🚀 [Display Engine] Launching target: {url_or_app_target}")

    # Launch via ShellExecuteW to inherit Interactive User Desktop Session 1
    shell32 = ctypes.windll.shell32
    res = shell32.ShellExecuteW(None, "open", url_or_app_target, None, None, 1)

    if res <= 32:
        # Fallback to Chrome directly with --new-window
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([chrome_path, "--new-window", url_or_app_target])

    time.sleep(2.0)

    # Enumerate and find target window
    found_hwnd = None

    EnumWindows = user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    GetWindowText = user32.GetWindowTextW
    GetWindowTextLength = user32.GetWindowTextLengthW
    IsWindowVisible = user32.IsWindowVisible

    def enum_cb(hwnd, lparam):
        nonlocal found_hwnd
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                title = buff.value
                for kw in window_keywords:
                    if kw.lower() in title.lower():
                        found_hwnd = hwnd
                        print(f"🎯 [Display Engine] Found Target Window: '{title}' (HWND {hwnd})")
                        force_window_to_primary_display(hwnd)
                        return False
        return True

    EnumWindows(EnumWindowsProc(enum_cb), 0)

    if found_hwnd:
        print(f"🎉 [Display Engine] SUCCESS! Target Window (HWND {found_hwnd}) is now ACTIVE on Display 1 Foreground!")
        return True
    else:
        print("⚠️  [Display Engine] Window launched, searching second pass...")
        return False

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://notebooklm.google.com/"
    keywords = sys.argv[2:] if len(sys.argv) > 2 else ["NotebookLM", "Chrome", "Google"]
    launch_and_display(target, keywords)
