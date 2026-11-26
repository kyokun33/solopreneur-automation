import os
import sys
import subprocess
import webbrowser

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_dynamic_viewer.html")
url = f"file:///{html_path.replace('\\', '/')}"

print(f"🚀 [고감독 다각도 모션 뷰어 팝업] 슈드용사 다각도 모션 뷰어를 전면 표출합니다: {html_path}")

# 1. Start browser directly
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    webbrowser.open(url, new=1)

# 2. Native startfile backup
os.startfile(html_path)

print("🎉 대표님 화면에 슈드용사 다각도 모션 뷰어 팝업 완수!")
