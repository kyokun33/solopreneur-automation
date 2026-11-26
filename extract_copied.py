import browser_cookie3
import shutil
import os

def extract_from_copied_db():
    cookie_db = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies")
    local_state = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Local State")
    temp_db = "temp_cookies.sqlite"
    
    shutil.copy2(cookie_db, temp_db)
    
    try:
        cj = browser_cookie3.chrome(cookie_file=temp_db, key_file=local_state, domain_name='.google.com')
        
        cookie_parts = []
        for cookie in cj:
            if 'google.com' in cookie.domain:
                cookie_parts.append(f"{cookie.name}={cookie.value}")
                
        if not cookie_parts:
            print("No google cookies found.")
            return
            
        cookie_string = "; ".join(cookie_parts)
        with open("notebooklm_cookies.txt", "w", encoding="utf-8") as f:
            f.write(cookie_string)
            
        print("Success! Extracted cookies into notebooklm_cookies.txt")
    except Exception as e:
        print("Failed:", e)

if __name__ == "__main__":
    extract_from_copied_db()
