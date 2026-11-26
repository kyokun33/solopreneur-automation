import json
from playwright.sync_api import sync_playwright

def get_notebooklm_cookies_from_profile():
    with sync_playwright() as p:
        print("Extracting cookies from saved profile...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./notebooklm_profile",
            headless=True
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/")
        page.wait_for_load_state("networkidle")
        
        cookies = browser.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        with open("notebooklm_cookies.txt", "w", encoding="utf-8") as f:
            f.write(cookie_string)
            
        print("Cookies successfully saved to notebooklm_cookies.txt")
        print("COOKIE_START")
        print(cookie_string)
        print("COOKIE_END")
        
        browser.close()

if __name__ == "__main__":
    get_notebooklm_cookies_from_profile()
