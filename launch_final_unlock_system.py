import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_final_unlock_system.html")
url = f"http://localhost:8000/sude_hero_final_unlock_system.html"

print(f"🚀 [고감독 최종 영웅 락온/해금 시스템 팝업] 대표님 모니터 전면에 슈드용사 V1 기본 영웅 & 5대 옵션 락온 해금 시스템을 엽니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

os.startfile(html_path)

print("🎉 대표님 화면 전면에 최종 락온/해금 시스템 시뮬레이터 팝업 완수!")
