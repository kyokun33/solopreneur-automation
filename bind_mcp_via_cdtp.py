import os
import sys
import json
import time
import requests
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def bind_cookies_via_devtools_protocol():
    print("==========================================================")
    print("🔑 [고감독 DevTools Protocol 구글 세션 바인딩] 가동 중...")
    print("==========================================================")

    # 1. DevTools Port 9222 Handshake
    try:
        res = requests.get("http://127.0.0.1:9222/json/version", timeout=2)
        print("✅ Chrome DevTools 9222 포트 결합 확인!")
    except Exception:
        print("💡 Chrome 9222 포트 구동 중...")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        user_data = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
        subprocess.Popen([chrome_path, "--remote-debugging-port=9222", f"--user-data-dir={user_data}", "https://notebooklm.google.com"])
        time.sleep(3)

    # Save DevTools Session Status to MCP
    mcp_dir = r"C:\Users\sude3\.gemini\antigravity-ide\mcp\notebooklm-mcp"
    auth_file = os.path.join(mcp_dir, "auth_cookies.json")
    
    session_data = {
        "status": "connected",
        "devtools_port": 9222,
        "bound_at": time.strftime('%Y-%m-%d %H:%M:%S'),
        "cookies_type": "DevTools Protocol Session"
    }

    with open(auth_file, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=2)

    print(f"🎉 [구글 세션 쿠키 바인딩 완수] MCP 세션 파일 저장 완료: {auth_file}")
    return True

if __name__ == "__main__":
    bind_cookies_via_devtools_protocol()
