import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_6heroes_motion_tester.html")
url = f"http://localhost:8000/sude_6heroes_motion_tester.html"

print(f"🚀 [고감독 6대 영웅 다각도 모션 테스트 베드 팝업] 대표님 모니터 전면에 슈드용사 6대 영웅 실시간 모션 테스트 베드를 엽니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

os.startfile(html_path)

print("🎉 대표님 화면 전면에 6대 영웅 실시간 모션 테스트 베드 팝업 완수!")
