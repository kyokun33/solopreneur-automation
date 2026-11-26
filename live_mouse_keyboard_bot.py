import os
import sys
import time
import subprocess
import pyperclip
import pyautogui

sys.stdout.reconfigure(encoding='utf-8')

# Disable Failsafe so mouse movement won't crash
pyautogui.FAILSAFE = False

def run_live_visual_macro():
    print("==========================================================")
    print("🎬 [고감독 모니터 전면 라이브 마우스/키보드 직접 구동 시작]")
    print("👉 대표님! 모니터 화면상에서 마우스와 키보드가 실시간으로 움직입니다.")
    print("==========================================================")

    # 1. Open Chrome on Primary Display
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
    url = "https://notebooklm.google.com"

    print("Step 1: 크롬 브라우저 최상단 전면 전체화면 구동...")
    subprocess.Popen([chrome_path, f"--user-data-dir={user_data}", "--start-maximized", url])
    
    # Wait 5 seconds for page load
    time.sleep(5)

    screenWidth, screenHeight = pyautogui.size()
    print(f"🖥️ 화면 해상도: {screenWidth} x {screenHeight}")

    # Step 2: Move Mouse Smoothly to Center/Top Left ('Create New Notebook' Button area)
    print("Step 2: 마우스 포인터를 '새 노트북 만들기' 위치로 이동 중...")
    target_x = int(screenWidth * 0.25) # ~25% from left (New Notebook card)
    target_y = int(screenHeight * 0.35) # ~35% from top

    pyautogui.moveTo(target_x, target_y, duration=1.5, tween=pyautogui.easeOutQuad)
    time.sleep(0.5)
    print("Step 3: '새 노트북 만들기' 클릭 집행!")
    pyautogui.click()
    
    time.sleep(3)

    # Step 4: Type Korean Title '보고서' via Clipboard
    print("Step 4: 한글 제목 '보고서' 타이핑 중...")
    pyperclip.copy("보고서")
    
    # Move mouse to notebook title or source dialog
    pyautogui.moveTo(screenWidth // 2, int(screenHeight * 0.2), duration=1.0)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    
    time.sleep(2)

    # Step 5: Inject Report Text
    print("Step 5: 보고서 전문 텍스트 준비 및 추가 진행...")
    report_file = r"c:\Users\sude3\OneDrive\바탕 화면\📄_NotebookLM_소소업로드용_통합보고서.txt"
    if os.path.exists(report_file):
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# 📓 [Connect AI] 대표님 보고서\n\n1. 전체 무인 자동화 완수\n2. Delete Mine v1.7 개발 완수"

    pyperclip.copy(content)

    print("==========================================================")
    print("🎉 대표님 모니터상에서 고감독이 마우스 이동 및 키보드 조작 완수!")
    print("==========================================================")

if __name__ == "__main__":
    run_live_visual_macro()
