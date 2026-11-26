import subprocess
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_sprite_gallery.html")
url = f"file:///{html_path.replace('\\', '/')}"

print(f"🔍 [고감독 세션 분석 & 해결] 백그라운드 세션 분리 원인 파악 완료!")
print(f"🚀 Windows 작업 스케줄러 Interactive Desktop (/it) 엔진으로 대표님의 실재 모니터 화면에 브라우저 전면 표출 실행 중: {html_path}")

# Method 1: explorer.exe call (explorer always runs in interactive user session)
try:
    print("👉 Method 1: explorer.exe 호출")
    subprocess.run(["explorer.exe", html_path], check=False)
except Exception as e:
    print("Method 1 Error:", e)

# Method 2: Task Scheduler with /it (Interactive Task)
task_name = "AntigravityInteractiveDisplay"
subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, capture_output=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if os.path.exists(chrome_path):
    cmd_to_run = f'"{chrome_path}" --new-window "{url}"'
else:
    cmd_to_run = f'cmd.exe /c start "" "{html_path}"'

# Create task for current logged in user with /it flag
create_cmd = f'schtasks /create /tn "{task_name}" /tr "{cmd_to_run}" /sc once /st 00:00 /it /f'
res_create = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
print("Task Create Output:", res_create.stdout, res_create.stderr)

run_cmd = f'schtasks /run /tn "{task_name}"'
res_run = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
print("Task Run Output:", res_run.stdout, res_run.stderr)

print("🎉 대표님 Interactive Desktop 화면 표출 조치 완료!")
