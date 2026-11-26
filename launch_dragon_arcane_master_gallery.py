import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_dragon_arcane_master_gallery.html")
url = f"http://localhost:8000/sude_dragon_arcane_master_gallery.html"

print(f"🚀 [고감독 대표님 양식 100% 도트 종합 시트 팝업] 대표님 모니터 전면에 Option 04 & 05 한글 도트 종합 마스터 시트 갤러리를 엽니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

os.startfile(html_path)

print("🎉 대표님 화면 전면에 한글 도트 종합 마스터 시트 갤러리 팝업 완수!")
