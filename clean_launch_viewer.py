import os
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_dynamic_viewer.html")
url = f"http://localhost:8000/sude_hero_dynamic_viewer.html"

print(f"🚀 [고감독 브라우저 세션 초기화 완료] 대표님 모니터 전면에 슈드용사 다각도 모션 뷰어를 깨끗하게 재오픈합니다.")
print(f"📁 대상 URL: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    print("✅ Chrome으로 새 창 구동 중...")
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
elif os.path.exists(edge_path):
    print("✅ Microsoft Edge로 새 창 구동 중...")
    cmd = [edge_path, "--new-window", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    print("✅ OS 기본 브라우저 구동 중...")
    os.system(f'start "" "{url}"')

time.sleep(1.0)
print("🎉 클린 브라우저 팝업 완료!")
