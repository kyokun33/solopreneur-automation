import os
import sys
import webbrowser
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:8000/sude_hero_sprite_gallery.html"
print(f"🚀 [고감독 강제 브라우저 표출] OS 기본 브라우저 및 파워셸을 통해 화면에 팝업창을 즉시 엽니다: {url}")

# 1. System Default Browser Open
webbrowser.open(url, new=1, autoraise=True)

# 2. PowerShell Start-Process Force Launch
ps_cmd = f'Start-Process "{url}"'
subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)

# 3. CMD Start Force Launch
os.system(f'start "" "{url}"')

print("🎉 기본 브라우저 강제 팝업 명령 3중 발사 완료!")
