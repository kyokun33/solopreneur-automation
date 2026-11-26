import os
import sys
import shutil
import sqlite3
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def extract_and_bind_google_cookies():
    print("==========================================================")
    print("🔑 [고감독 구글 세션 쿠키 연동 파이프라인] 구동 중...")
    print("==========================================================")

    src_cookie = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"
    if not os.path.exists(src_cookie):
        src_cookie = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data\Default\Cookies"

    dst_cookie = os.path.join(os.getcwd(), "temp_sync_cookies.db")

    # Use PowerShell force copy to avoid file lock
    ps_cmd = f"Copy-Item -Path '{src_cookie}' -Destination '{dst_cookie}' -Force"
    try:
        subprocess.run(["powershell", "-Command", ps_cmd], check=True)
        print("✅ [단계 1] 크롬 쿠키 DB 파일 락 해제 복사 완료!")
    except Exception as e:
        print(f"❌ 파워쉘 복사 예외: {e}")
        return False

    if not os.path.exists(dst_cookie):
        print("❌ 복사된 DB 파일 미감지")
        return False

    cookies_dict = {}
    try:
        conn = sqlite3.connect(dst_cookie)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%google.com%'")
        rows = cursor.fetchall()

        for name, val in rows:
            if name in ['SID', 'HSID', 'SSID', '__Secure-1PSID', '__Secure-3PSID', 'SAPISID', 'APISID']:
                if val:
                    cookies_dict[name] = val

        conn.close()
        try: os.remove(dst_cookie)
        except Exception: pass

        if not cookies_dict:
            print("⚠️ 크롬 DB에서 텍스트 쿠키 값이 직접 읽히지 않음 (DPAPI 암호화 상태).")
            print("💡 DevTools 9222 포트 메모리 세션 파이프라인 연결로 우회 진행...")
            return False

        # Format cookie string
        cookie_header = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
        print(f"🎉 [단계 2] 구글 세션 쿠키 {len(cookies_dict)}개 추출 완료!")

        # Save to MCP auth config file
        mcp_dir = r"C:\Users\sude3\.gemini\antigravity-ide\mcp\notebooklm-mcp"
        auth_file = os.path.join(mcp_dir, "auth_cookies.json")
        with open(auth_file, "w", encoding="utf-8") as f:
            json.dump({"cookies": cookies_dict, "cookie_header": cookie_header}, f, indent=2)

        print(f"✅ [단계 3] MCP 디렉터리에 구글 세션 쿠키 바인딩 완수: {auth_file}")
        return True

    except Exception as e:
        print(f"❌ 쿠키 파싱 실패: {e}")
        return False

if __name__ == "__main__":
    extract_and_bind_google_cookies()
