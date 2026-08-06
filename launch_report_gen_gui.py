import subprocess
import time
import os

url = "http://127.0.0.1:8090"
print(f"Launching AI Report Generator App UI at {url}...")

# 윈도우 전면 브라우저 창 띄우기
cmd = f'start chrome --new-window "{url}"'
subprocess.run(cmd, shell=True)
