import subprocess
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_sprite_gallery.html")
url_file = f"file:///{html_path.replace('\\', '/')}"
url_http = "http://localhost:8000/sude_hero_sprite_gallery.html"

print(f"🚀 [고감독 독립 GUI 프로세스 런처] DETACHED_PROCESS 플래그로 대표님 모니터에 크롬/엣지 창을 전면 팝업합니다.")

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

browser_binary = None
for p in chrome_paths:
    if os.path.exists(p):
        browser_binary = p
        break

DETACHED_PROCESS = 0x00000008
CREATE_NEW_CONSOLE = 0x00000010

if browser_binary:
    print(f"✅ 브라우저 바이너리 발견: {browser_binary}")
    # Launch detached GUI browser
    cmd = [browser_binary, "--new-window", "--start-maximized", url_http]
    p = subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
    print(f"🚀 프로세스 실행 완료 (PID: {p.pid})")
else:
    print("⚠️ 기본 브라우저 명령으로 실행 시도")
    cmd = f'start "" "{url_http}"'
    subprocess.Popen(cmd, shell=True, creationflags=DETACHED_PROCESS)

# Also launch file directly via explorer detached
cmd_exp = ["explorer.exe", html_path]
subprocess.Popen(cmd_exp, creationflags=DETACHED_PROCESS)

print("🎉 독립 GUI 프로세스로 브라우저 전면 표출 완료!")
