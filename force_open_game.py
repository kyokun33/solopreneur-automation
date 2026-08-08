import subprocess
import time
import os

print("1. Opening Chrome window with game URL...")
url = "http://localhost:3000/rogue_project/index.html"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Launch via start command in cmd to force new tab/window open in default browser session
subprocess.run(f'start "" "{chrome_path}" --new-window "{url}"', shell=True)
