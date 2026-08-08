import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = os.path.expanduser(r"~\.notebooklm-mcp\chrome-profile")
os.makedirs(user_data, exist_ok=True)

cmd = [
    chrome_path,
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    f"--user-data-dir={user_data}",
    "https://notebooklm.google.com/"
]

print("Launching Chrome with Remote Debugging Port 9222...")
subprocess.Popen(cmd)
