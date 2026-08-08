import subprocess
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = sys.argv[1] if len(sys.argv) > 1 else "https://notebooklm.google.com/"

print(f"🚀 [Windows Task Scheduler Engine] 대표님 사용자 세션(Interactive Desktop)으로 브라우저 직격 구동 중: {url}")

# Create one-time instant scheduled task in interactive user session
task_name = "AntigravityDisplayTask"

# Delete existing task if present
subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, capture_output=True)

# Create task to run chrome with url in interactive session (/it = Interactive Task)
chrome_cmd = f'\\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\\" --new-window \\"{url}\\"'
create_cmd = f'schtasks /create /tn "{task_name}" /tr "{chrome_cmd}" /sc once /st 00:00 /it /f'
subprocess.run(create_cmd, shell=True, capture_output=True)

# Run task immediately
run_cmd = f'schtasks /run /tn "{task_name}"'
res = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)

print("Task Run Output:", res.stdout)
time.sleep(2.0)
