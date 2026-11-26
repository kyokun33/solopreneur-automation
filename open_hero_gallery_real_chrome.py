import subprocess
import time
import ctypes
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:8000/sude_hero_sprite_gallery.html"

print(f"🚀 [고감독 100% 모니터 전면 표출] 대표님 크롬 브라우저를 주 모니터(Display 1) 최상단에 전면 배치합니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

cmd = [chrome_path, "--new-window", "--start-maximized", url]
subprocess.Popen(cmd)

time.sleep(2.0)

user32 = ctypes.windll.user32
SW_RESTORE = 9
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002

def bring_chrome_to_foreground():
    EnumWindows = user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    GetWindowText = user32.GetWindowTextW
    GetWindowTextLength = user32.GetWindowTextLengthW
    IsWindowVisible = user32.IsWindowVisible

    target_hwnd = None

    def enum_cb(hwnd, lparam):
        nonlocal target_hwnd
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                title = buff.value
                if "슈드용사" in title or "Chrome" in title or "갤러리" in title or "localhost" in title:
                    print(f"✅ 발견된 크롬 창: hwnd={hwnd}, title={title}")
                    target_hwnd = hwnd
                    # Bring to top of display 1
                    user32.ShowWindow(hwnd, SW_RESTORE)
                    user32.SetForegroundWindow(hwnd)
                    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 1600, 950, 0)
                    time.sleep(0.2)
                    user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 1600, 950, 0)
        return True

    EnumWindows(EnumWindowsProc(enum_cb), 0)
    return target_hwnd

brought = bring_chrome_to_foreground()
if brought:
    print("🎉 대표님의 주 모니터 전면(Display 1, 좌표 0,0) 표출 완전 성공!")
else:
    print("⚠️ 크롬 창을 찾는 도중 전면 전환 작업을 재시도합니다.")
