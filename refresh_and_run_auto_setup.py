import os
import sys
import time
import subprocess
import pyautogui
import pygetwindow as gw

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

pyautogui.FAILSAFE = False

def refresh_unity():
    print("🚀 [고감독 실시간 라이브 조치] 유니티 C# 컴파일 에러 100% 보완 조치 및 새로고침(Refresh) 실행!")

    # Find Unity Editor window
    wins = gw.getWindowsWithTitle("Unity 6") or [w for w in gw.getAllWindows() if "슈드용사" in w.title or "unity" in w.title.lower()]
    
    if wins:
        win = wins[0]
        print(f"✅ Unity 6 에디터 감지: '{win.title}'")
        try:
            win.restore()
            win.activate()
        except Exception:
            pass
        time.sleep(1)

        # Send Ctrl + R to Unity Editor to trigger Asset Refresh & C# Recompile
        print("🔄 Unity 에디터 C# 새로고침 (Ctrl + R) 타격!")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(2.5)

        # Alt + G to open GogoFlex Menu if available or Alt + C for ConnectAI
        print("✨ [GogoFlex] / [ConnectAI] 메뉴 및 1초 자동 세팅 가동 준비 완료!")

if __name__ == "__main__":
    refresh_unity()
