import json
from playwright.sync_api import sync_playwright

def get_notebooklm_cookies():
    user_data_dir = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
    
    with sync_playwright() as p:
        print("Launching browser to extract cookies...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,  # Headless false to allow login if needed
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/")
        page.wait_for_load_state("networkidle")
        
        cookies = browser.cookies()
        
        # Format cookies into a string for the Cookie header
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        print("COOKIE_START")
        print(cookie_string)
        print("COOKIE_END")
        
        browser.close()

if __name__ == "__main__":
    get_notebooklm_cookies()
