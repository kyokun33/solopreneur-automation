import sys
import time
import pyautogui
import pygetwindow as gw

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

pyautogui.FAILSAFE = False

def play_unity():
    print("🎮 [고감독] 유니티 에디터 실행 상태 점검 및 Play(▶) 모드 직접 클릭 가동!")
    
    wins = gw.getWindowsWithTitle("Unity 6") or [w for w in gw.getAllWindows() if "슈드용사" in w.title or "unity" in w.title.lower()]
    
    if wins:
        win = wins[0]
        print(f"✅ Unity 6 에디터 감지: '{win.title}'")
        try:
            win.restore()
            win.activate()
        except Exception as e:
            print(f"Window activate note: {e}")
        time.sleep(1)

        # Force refresh and compile check first
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(2)

        # Trigger Play Mode Ctrl + P
        print("▶️ 유니티 플레이(Ctrl + P) 직접 타격!")
        pyautogui.hotkey('ctrl', 'p')
        time.sleep(2)
        print("🎉 유니티 플레이 모드 신호 발송 완료!")
    else:
        print("⚠️ Unity 에디터 창을 찾을 수 없습니다.")

if __name__ == "__main__":
    play_unity()
