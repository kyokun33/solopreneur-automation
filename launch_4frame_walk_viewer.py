import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_4frame_walk_viewer.html")
url = f"http://localhost:8000/sude_4frame_walk_viewer.html"

print(f"🚀 [고감독 대표님 모니터 전면 팝업] 대표님 원본 캐릭터 4프레임 걷기 모션 대시보드 팝업: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

os.startfile(html_path)

print("🎉 대표님 모니터 최상단 전면에 4프레임 걷기 모션 대시보드 팝업 완료!")
