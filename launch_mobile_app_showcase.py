import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:8000/delete_mine_mobile_app.html"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DETACHED_PROCESS = 0x00000008

print(f"🚀 [고감독 대표님 모니터 전면 팝업] 모바일 앱 개발 역량 쇼케이스 팝업: {url}")

if os.path.exists(chrome_path):
    subprocess.Popen([chrome_path, "--new-window", "--start-maximized", url], creationflags=DETACHED_PROCESS)
else:
    os.system(f'start chrome "{url}"')

print("🎉 모바일 앱 쇼케이스 표출 완료!")
