import subprocess
import os
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.expanduser(r"~\.notebooklm-mcp\chrome-profile")

subprocess.run("taskkill /F /IM chrome.exe", shell=True, capture_output=True)
time.sleep(1)

cmd = [
    chrome_path,
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    f"--user-data-dir={user_data}",
    "https://notebooklm.google.com/"
]

print("Launching Chrome with Remote Debugging (Port 9222)...")
subprocess.Popen(cmd)
