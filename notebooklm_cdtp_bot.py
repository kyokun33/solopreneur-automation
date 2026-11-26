import os
import sys
import time
import subprocess
import requests

sys.stdout.reconfigure(encoding='utf-8')

def launch_chrome_with_remote_debugging():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
    url = "https://notebooklm.google.com"

    print("🚀 [고감독 무인 크롬 디버깅 포트 오픈] 로그인 세션 유지 모드로 구동 중...")
    
    cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--start-maximized",
        url
    ]
    
    try:
        subprocess.Popen(cmd)
        print("✅ 구글 크롬(세션 보존 9222 포트)이 대표님 모니터 전면에 구동되었습니다!")
    except Exception as e:
        print(f"❌ 크롬 구동 실패: {e}")

if __name__ == "__main__":
    launch_chrome_with_remote_debugging()
