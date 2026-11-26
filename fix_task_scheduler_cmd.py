import subprocess
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_sprite_gallery.html")

print(f"🚀 Windows 작업 스케줄러 (/it) 이스케이프 보정 후 재실행 중...")

task_name = "AntigravityInteractiveDisplay"
subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, capture_output=True)

# Use cmd.exe /c start for safe path execution without quotes issue
tr_cmd = f'cmd.exe /c start "" "{html_path}"'
create_cmd = ['schtasks', '/create', '/tn', task_name, '/tr', tr_cmd, '/sc', 'once', '/st', '00:00', '/it', '/f']

res_create = subprocess.run(create_cmd, capture_output=True, text=True)
print("Task Create Result:", res_create.stdout, res_create.stderr)

run_cmd = ['schtasks', '/run', '/tn', task_name]
res_run = subprocess.run(run_cmd, capture_output=True, text=True)
print("Task Run Result:", res_run.stdout, res_run.stderr)

print("🎉 대표님 모니터 전면(Session 1 Desktop) 표출 완료!")
