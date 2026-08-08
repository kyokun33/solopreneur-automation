import subprocess
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = sys.argv[1] if len(sys.argv) > 1 else "https://notebooklm.google.com/"

print(f"🚀 [User Session Direct Injection] 대표님의 Session 1 데스크톱으로 브라우저 직격 투입 중: {url}")

ps_script = f'''
$action = New-ScheduledTaskAction -Execute "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" -Argument "--new-window \\"{url}\\""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(1)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AntigravityUserTask" -Action $action -Trigger $trigger -Settings $settings -User "$env:USERNAME" -Force
Start-ScheduledTask -TaskName "AntigravityUserTask"
'''

with open("run_user_task.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

subprocess.run("powershell -ExecutionPolicy Bypass -File run_user_task.ps1", shell=True)
time.sleep(2.5)
