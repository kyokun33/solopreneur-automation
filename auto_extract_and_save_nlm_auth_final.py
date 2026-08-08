import os
import sys
import json
import shutil
import time
from playwright.sync_api import sync_playwright

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

print("[Auto Auth Extractor] Extracting Chrome session cookies...")

user_data_dir = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
temp_profile_dir = r"C:\Users\sude3\AppData\Local\Temp\chrome_shadow_profile_nlm"

if os.path.exists(temp_profile_dir):
    try:
        shutil.rmtree(temp_profile_dir)
    except Exception as e:
        print(f"Temp profile clean note: {e}")

print("Copying Chrome profile data...")
try:
    shutil.copytree(
        user_data_dir,
        temp_profile_dir,
        ignore=shutil.ignore_patterns("Default\\Cache*", "Default\\Code Cache*", "Crashpad", "BrowserMetrics*")
    )
except Exception as e:
    print(f"Copy note: {e}")

with sync_playwright() as p:
    print("Launching browser context...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=temp_profile_dir,
        headless=True,
        channel="chrome",
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = context.pages[0] if context.pages else context.new_page()
    
    print("Navigating to https://notebooklm.google.com/ ...")
    page.goto("https://notebooklm.google.com/", wait_until="networkidle", timeout=60000)
    time.sleep(3)

    current_url = page.url
    print(f"Current URL: {current_url}")

    csrf_token = ""
    try:
        csrf_token = page.evaluate("() => window.WIZ_global_data?.SNlM0e || ''")
    except Exception as e:
        print(f"CSRF eval note: {e}")

    cookies_list = context.cookies()
    cookies_dict = {}
    for c in cookies_list:
        if "google.com" in c["domain"] or "notebooklm" in c["domain"]:
            cookies_dict[c["name"]] = c["value"]

    print(f"Extracted cookies count: {len(cookies_dict)}")
    print(f"Extracted CSRF token: {csrf_token[:15]}..." if csrf_token else "CSRF token empty")

    context.close()

    auth_dir = os.path.expanduser("~/.notebooklm-mcp")
    os.makedirs(auth_dir, exist_ok=True)
    auth_path = os.path.join(auth_dir, "auth.json")

    auth_data = {
        "cookies": cookies_dict,
        "csrf_token": csrf_token,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    with open(auth_path, "w", encoding="utf-8") as f:
        json.dump(auth_data, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: Saved auth.json to {auth_path}")
