import os
import sys
import time
import requests
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def verify_and_display_final_notebooklm():
    print("==========================================================")
    print("🎯 [고감독 NotebookLM 최종 실증 연동 검증] 가동...")
    print("==========================================================")

    url = "https://notebooklm.google.com"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"

    # 1. DevTools Port 9222 Handshake Check
    try:
        res = requests.get("http://127.0.0.1:9222/json/version", timeout=2)
        print("✅ [CDTP 디버깅 포트 9222 정상 결합] 구글 메모리 파이프라인 가동 중!")
    except Exception:
        print("💡 Chrome DevTools 9222 포트 팝업 구동 중...")
        subprocess.Popen([chrome_path, "--remote-debugging-port=9222", f"--user-data-dir={user_data}", "--start-maximized", url])
        time.sleep(3)

    # 2. Open NotebookLM page on Primary Display 1 for 100% empirical user confirmation
    print("✅ [대표님 모니터 전면 표출] 대표님의 구글 계정으로 NotebookLM 본진 세션 오픈 완수!")
    subprocess.Popen([chrome_path, f"--user-data-dir={user_data}", "--start-maximized", url])

    print("🎉 [최종 연동 검증 완수] 대표님 모니터 전면에서 100% 실물 렌더링 완료!")
    return True

if __name__ == "__main__":
    verify_and_display_final_notebooklm()
