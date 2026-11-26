import json
from playwright.sync_api import sync_playwright
import os
import sys

def get_notebooklm_cookies_manual():
    with sync_playwright() as p:
        print("Launching actual Google Chrome for manual login...", flush=True)
        
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            print(f"Error: Chrome not found at {chrome_path}", flush=True)
            return
            
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir="./notebooklm_profile",
                executable_path=chrome_path,
                headless=False,
                no_viewport=True,
                args=[
                    "--start-maximized", 
                    "--window-position=0,0", 
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            print("Browser launched.", flush=True)
        except Exception as e:
            print("Failed to launch browser:", e, flush=True)
            return
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/")
        page.bring_to_front()
        
        print("Please log in to your Google Account in the opened browser window.", flush=True)
        print("Waiting for you to reach the NotebookLM dashboard...", flush=True)
        
        try:
            page.wait_for_url("https://notebooklm.google.com/**", timeout=300000)
            page.wait_for_load_state("networkidle", timeout=300000)
            print("Login seems successful. Extracting cookies...", flush=True)
        except Exception as e:
            print("Timed out or error waiting for login:", e, flush=True)
            
        cookies = browser.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        with open("notebooklm_cookies.txt", "w", encoding="utf-8") as f:
            f.write(cookie_string)
            
        print("Cookies successfully saved to notebooklm_cookies.txt", flush=True)
        browser.close()

if __name__ == "__main__":
    get_notebooklm_cookies_manual()
