import browser_cookie3
import traceback

def extract_notebooklm_cookies():
    try:
        print("Attempting to load Chrome cookies...")
        cj = browser_cookie3.chrome(domain_name='.google.com')
        
        cookie_parts = []
        for cookie in cj:
            if 'google.com' in cookie.domain:
                cookie_parts.append(f"{cookie.name}={cookie.value}")
                
        if not cookie_parts:
            print("No google cookies found.")
            return
            
        cookie_string = "; ".join(cookie_parts)
        print("COOKIE_START")
        print(cookie_string)
        print("COOKIE_END")
        
    except Exception as e:
        print("Error extracting cookies:")
        traceback.print_exc()

if __name__ == "__main__":
    extract_notebooklm_cookies()
