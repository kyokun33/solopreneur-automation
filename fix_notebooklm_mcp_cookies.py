import os
import sys
import subprocess
import sqlite3

sys.stdout.reconfigure(encoding='utf-8')

def extract_cookies_with_powershell_bypass():
    print("==========================================================")
    print("🛠️ [고감독 바이패스 파이프라인] PowerShell 강제 공유 복사 가동...")
    print("==========================================================")

    src_cookie = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"
    dst_cookie = os.path.join(os.getcwd(), "bypassed_chrome_cookies.db")

    ps_cmd = f"Copy-Item -Path '{src_cookie}' -Destination '{dst_cookie}' -Force"
    
    try:
        subprocess.run(["powershell", "-Command", ps_cmd], check=True)
        print("✅ [파일 락 100% 바이패스 성공] 윈도우 크롬 쿠키 DB 강제 사본 복사 완수!")
    except Exception as e:
        print(f"❌ 파워쉘 강제 복사 예외: {e}")
        return None

    if not os.path.exists(dst_cookie):
        print("❌ 바이패스 DB 미감지")
        return None

    cookies = {}
    try:
        conn = sqlite3.connect(dst_cookie)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%google.com%'")
        rows = cursor.fetchall()
        
        for name, val in rows:
            if name in ['SID', 'HSID', 'SSID', '__Secure-1PSID', '__Secure-3PSID', 'SAPISID', 'APISID']:
                cookies[name] = val

        conn.close()
        try: os.remove(dst_cookie)
        except Exception: pass

        print(f"🎉 [구글 세션 쿠키 수집 완료] 총 {len(cookies)}개 세션 키 바이패스 안착!")
        for k in cookies.keys():
            print(f"   - {k}: 100% 바인딩 성공")
        return cookies
    except Exception as e:
        print(f"❌ DB 읽기 예외: {e}")
        return None

if __name__ == "__main__":
    extract_cookies_with_powershell_bypass()
