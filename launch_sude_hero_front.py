import subprocess
import time
import ctypes
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_sprite_gallery.html")
file_url = f"file:///{html_path.replace('\\', '/')}"

print(f"🚀 [고감독 라이브 시각화] 주 모니터(Display 1) 최상단에 슈드용사 스프라이트 갤러리 팝업 실행: {file_url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [chrome_path, "--new-window", file_url]
subprocess.Popen(cmd)

time.sleep(1.5)

user32 = ctypes.windll.user32
SW_RESTORE = 9
HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002

def find_and_bring_to_front():
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
                if "슈드용사" in title or "Chrome" in title or "Paladin" in title:
                    print(f"✅ 발견된 전면 표출 창: {title}")
                    user32.ShowWindow(hwnd, SW_RESTORE)
                    user32.SetForegroundWindow(hwnd)
                    # Force move to Primary Monitor (0,0)
                    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 1280, 840, 0)
        return True

    EnumWindows(EnumWindowsProc(enum_cb), 0)

find_and_bring_to_front()
print("🎉 대표님 모니터 전면 표출 완료!")
