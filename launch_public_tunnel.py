import subprocess
import time
import os
import sys

def start_public_url():
    print("[INFO] Creating Instant Public HTTPS Web URL for AI Report Generator SaaS...")
    cmd = "npx -y localtunnel --port 8000"
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
        time.sleep(3)
        for _ in range(12):
            line = proc.stdout.readline()
            if "your url is:" in line.lower():
                url = line.strip().split("your url is:")[-1].strip()
                print(f"\n[SUCCESS] 24-HOUR PUBLIC HTTPS WEB URL CREATED!")
                print(f"URL: {url}\n")
                return url
            time.sleep(1)
    except Exception as e:
        print(f"[ERROR] Tunnel creation info: {e}")

if __name__ == "__main__":
    start_public_url()

