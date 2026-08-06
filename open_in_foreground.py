import subprocess
import time
import os

html_path = os.path.abspath(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ebook_reader.html")
file_url = f"file:///{html_path.replace(os.sep, '/')}"

print(f"Launching Edge in App mode for: {file_url}")

# Try MS Edge first
try:
    subprocess.Popen(["cmd.exe", "/c", "start", "msedge", f"--app={file_url}"])
    print("MS Edge launched!")
except Exception as e:
    print(f"Edge launch error: {e}")

# Also try Chrome
try:
    subprocess.Popen(["cmd.exe", "/c", "start", "chrome", f"--app={file_url}"])
    print("Chrome launched!")
except Exception as e:
    print(f"Chrome launch error: {e}")

# Default browser fallback
try:
    os.startfile(html_path)
    print("os.startfile executed!")
except Exception as e:
    print(f"os.startfile error: {e}")
