import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 [고감독 대표님 모니터 전면 강력 팝업] Delete Mine GUI 앱 및 웹 대시보드 2중 표출 가동...")

# 1. Open Web Dashboard in Chrome (Primary Display 1 Foreground)
url = "http://localhost:8000/delete_mine_web_viewer.html"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    subprocess.Popen([chrome_path, "--new-window", "--start-maximized", url], creationflags=DETACHED_PROCESS)
else:
    os.system(f'start chrome "{url}"')

# 2. Open Desktop PyQt6 GUI App
pythonw_path = os.path.join(sys.prefix, "pythonw.exe")
script_path = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\delete_mine_app.py"

if os.path.exists(pythonw_path):
    subprocess.Popen([pythonw_path, script_path], creationflags=DETACHED_PROCESS)

# 3. Open Explorer Folder directly
os.system(f'explorer.exe /select,"{script_path}"')

print("🎉 대표님 모니터 전면에 Delete Mine 프로그램 및 대시보드 표출 성공!")
