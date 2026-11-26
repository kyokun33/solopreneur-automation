import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("comfyui_integration_hub.html")
url = f"http://localhost:8000/comfyui_integration_hub.html"

print(f"🚀 [고감독 대표님 모니터 전면 팝업] 대표님 화면 최상단 전면에 ComfyUI & Manager 통합 연동 센터를 엽니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

os.startfile(html_path)

print("🎉 대표님 모니터 최상단 전면에 ComfyUI & Manager 연동 센터 팝업 완수!")
