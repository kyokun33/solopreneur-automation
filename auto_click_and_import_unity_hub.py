import ctypes
import os
import sys
import time
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

user32 = ctypes.windll.user32
PROJECT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

def copy_to_clipboard(text):
    cmd = 'choice /C Y /N /D Y /T 0 > NUL'
    subprocess.run(f'echo | set /p="{text}" | clip', shell=True)

def find_unity_hub_hwnd():
    target_hwnd = []
    
    def enum_cb(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if "unity hub" in title.lower() or title.lower() == "hub":
                target_hwnd.append(hwnd)
        return True

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(CMPFUNC(enum_cb), 0)
    return target_hwnd[0] if target_hwnd else None

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

def click_point(x, y):
    user32.SetCursorPos(x, y)
    time.sleep(0.1)
    user32.mouse_event(0x0002, 0, 0, 0, 0) # MOUSEEVENTF_LEFTDOWN
    time.sleep(0.05)
    user32.mouse_event(0x0004, 0, 0, 0, 0) # MOUSEEVENTF_LEFTUP

def press_keys_ctrl_v():
    user32.keybd_event(0x11, 0, 0, 0) # VK_CONTROL
    user32.keybd_event(0x56, 0, 0, 0) # 'V'
    time.sleep(0.05)
    user32.keybd_event(0x56, 0, 0x0002, 0)
    user32.keybd_event(0x11, 0, 0x0002, 0)

def press_enter():
    user32.keybd_event(0x0D, 0, 0, 0) # VK_RETURN
    time.sleep(0.05)
    user32.keybd_event(0x0D, 0, 0x0002, 0)

def run_import_automation():
    print("🚀 [고감독 실시간 라이브 UI 시각화] Unity Hub 프로젝트 임포트 자동 타격 시작!")
    copy_to_clipboard(PROJECT_PATH)

    hwnd = find_unity_hub_hwnd()
    if not hwnd:
        print("🌐 Unity Hub 창 탐색 실패, Unity Hub 프로세스를 전면에 실행합니다...")
        subprocess.Popen([r"C:\Program Files\Unity Hub\Unity Hub.exe"])
        time.sleep(2.5)
        hwnd = find_unity_hub_hwnd()

    if not hwnd:
        print("⚠️ Unity Hub HWND를 찾을 수 없습니다.")
        return

    # Bring Unity Hub to foreground
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.8)

    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    width = right - left
    height = bottom - top

    print(f"🎯 Unity Hub 창 위치 감지: ({left}, {top}), 크기: {width}x{height}")

    # 1. Try Clicking '프로젝트 임포트' Center Button (~54% width, ~69% height)
    import_btn_x = left + int(width * 0.54)
    import_btn_y = top + int(height * 0.69)

    print(f"💥 '프로젝트 임포트' 중앙 버튼 클릭 타격! ({import_btn_x}, {import_btn_y})")
    click_point(import_btn_x, import_btn_y)
    time.sleep(1.5)

    # 2. Also Click Top-Right '추가 ∨' Button (~86% width, ~19% height) as Backup
    add_btn_x = left + int(width * 0.86)
    add_btn_y = top + int(height * 0.19)

    print(f"💥 '추가 ∨' 상단 버튼 클릭 타격! ({add_btn_x}, {add_btn_y})")
    click_point(add_btn_x, add_btn_y)
    time.sleep(1.2)

    # If dropdown menu appeared, click '디스크에서 프로젝트 추가' (slight below add_btn_y)
    click_point(add_btn_x, add_btn_y + 40)
    time.sleep(1.5)

    # 3. Paste project path into Windows File Dialog & press Enter
    print(f"✍️ 파일 선택 창에 '슈드용사' 경로 주입: {PROJECT_PATH}")
    press_keys_ctrl_v()
    time.sleep(0.5)
    press_enter()
    time.sleep(1.0)
    press_enter()
    time.sleep(1.0)
    press_enter()

    print("🎉 Unity Hub '슈드용사' 프로젝트 임포트 클릭 및 경로 주입 타격 완수!")

if __name__ == "__main__":
    run_import_automation()
