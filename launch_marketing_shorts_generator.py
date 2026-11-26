import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

url = f"http://localhost:8001/"

print(f"🚀 [고감독 대표님 모니터 전면 팝업] 대표님 화면 최상단 전면에 AI 자동 숏츠 & 마케팅 제작기 대시보드를 엽니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

print("🎉 대표님 모니터 최상단 전면에 AI 자동 숏츠 & 마케팅 제작기 팝업 완료!")
