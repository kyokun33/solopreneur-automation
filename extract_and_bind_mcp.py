import os
import sys
import json
import browser_cookie3

sys.stdout.reconfigure(encoding='utf-8')

def extract_cookies_and_bind_to_mcp():
    print("==========================================================")
    print("🔑 [고감독 browser-cookie3 구글 세션 추출 & MCP 연동] 가동...")
    print("==========================================================")

    try:
        cj = browser_cookie3.chrome(domain_name='.google.com')
        google_cookies = {}
        for c in cj:
            if c.name in ['SID', 'HSID', 'SSID', '__Secure-1PSID', '__Secure-3PSID', 'SAPISID', 'APISID']:
                google_cookies[c.name] = c.value

        print(f"🎉 [구글 크롬 세션 수집 완수] 추출된 구글 인증 키: {len(google_cookies)}개")
        for k, v in google_cookies.items():
            print(f"   - {k}: {v[:8]}... (바인딩 완료)")

        cookie_str = "; ".join([f"{k}={v}" for k, v in google_cookies.items()])

        # Save to MCP directory
        mcp_dir = r"C:\Users\sude3\.gemini\antigravity-ide\mcp\notebooklm-mcp"
        auth_file = os.path.join(mcp_dir, "auth_cookies.json")
        with open(auth_file, "w", encoding="utf-8") as f:
            json.dump({"cookies": google_cookies, "cookie_header": cookie_str}, f, indent=2)

        print(f"✅ [MCP 세션 파일 바인딩 완료]: {auth_file}")
        return True

    except Exception as e:
        print(f"❌ browser_cookie3 예외: {e}")
        return False

if __name__ == "__main__":
    extract_cookies_and_bind_to_mcp()
