import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def get_notebooklm_cookies_selenium():
    print("Launching visible Chrome with Selenium...", flush=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Use a temporary user data dir so it doesn't conflict with main Chrome
    options.add_argument("--user-data-dir=./notebooklm_selenium_profile")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print("Failed to start Selenium WebDriver:", e)
        return
        
    driver.get("https://notebooklm.google.com/")
    print("Browser launched. Please log in.", flush=True)
    
    # Wait until user logs in and the URL shows dashboard
    try:
        WebDriverWait(driver, 300).until(
            lambda d: "notebooklm.google.com" in d.current_url and "accounts.google.com" not in d.current_url
        )
        print("Login successful. Saving cookies...", flush=True)
    except Exception as e:
        print("Timeout waiting for login.", flush=True)
        
    cookies = driver.get_cookies()
    cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    
    with open("notebooklm_cookies.txt", "w", encoding="utf-8") as f:
        f.write(cookie_string)
        
    print("Cookies successfully saved to notebooklm_cookies.txt", flush=True)
    driver.quit()

if __name__ == "__main__":
    get_notebooklm_cookies_selenium()
