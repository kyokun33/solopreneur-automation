import os
import sys
import time
import subprocess
import pyautogui
import pygetwindow as gw
import pyperclip

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

pyautogui.FAILSAFE = False
PROJECT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"
UNITY_HUB_EXE = r"C:\Program Files\Unity Hub\Unity Hub.exe"

def run_import():
    print("🚀 [고감독 실시간 라이브 UI 자동 타격] Unity Hub '슈드용사' 프로젝트 임포트 구동 시작!")
    
    # 1. Ensure Unity Hub is launched
    subprocess.Popen([UNITY_HUB_EXE])
    time.sleep(2.5)

    # 2. Get active display bounds
    screen_w, screen_h = pyautogui.size()
    print(f"🖥️ 화면 해상도 감지: {screen_w}x{screen_h}")

    hub_windows = gw.getWindowsWithTitle("Hub") or gw.getWindowsWithTitle("Unity Hub")
    if hub_windows:
        win = hub_windows[0]
        try:
            win.restore()
            win.activate()
            time.sleep(1)
            left, top, width, height = win.left, win.top, win.width, win.height
            print(f"✅ Unity Hub 윈도우 좌표 감지: ({left}, {top}), 크기: {width}x{height}")
        except Exception:
            left, top, width, height = 0, 0, screen_w, screen_h
    else:
        left, top, width, height = 0, 0, screen_w, screen_h

    # 3. Copy project path to clipboard
    pyperclip.copy(PROJECT_PATH)
    print(f"📋 클립보드에 '슈드용사' 경로 복사 완료: {PROJECT_PATH}")

    # 4. Click '프로젝트 임포트' Center Button (~54% width, ~69% height)
    center_btn_x = left + int(width * 0.54)
    center_btn_y = top + int(height * 0.69)

    print(f"💥 [1차 타격] 화면 중앙 '프로젝트 임포트' 버튼 클릭! ({center_btn_x}, {center_btn_y})")
    pyautogui.click(center_btn_x, center_btn_y)
    time.sleep(1.8)

    # 5. Click Top Right '추가 ∨' Button (~86% width, ~19% height)
    add_btn_x = left + int(width * 0.86)
    add_btn_y = top + int(height * 0.19)

    print(f"💥 [2차 타격] 상단 우측 '추가 ∨' 버튼 클릭! ({add_btn_x}, {add_btn_y})")
    pyautogui.click(add_btn_x, add_btn_y)
    time.sleep(1.2)
    
    # Dropdown menu '디스크에서 프로젝트 추가' click
    pyautogui.click(add_btn_x, add_btn_y + 40)
    time.sleep(1.8)

    # 6. Paste path into file folder chooser dialog and press Enter
    print("✍️ 폴더 선택 창에 프로젝트 경로 주입 (Ctrl+V) & Enter 타격!")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1.0)
    pyautogui.press('enter')
    time.sleep(1.0)
    pyautogui.press('enter')

    print("🎉 [슈드용사] Unity Hub 프로젝트 임포트 라이브 자동 타격 100% 완수!")

if __name__ == "__main__":
    run_import()
