import os
import sys
import json
import sqlite3
import shutil
import base64
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_DATA_DIR = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
LOCAL_STATE_PATH = os.path.join(USER_DATA_DIR, "Local State")
COOKIES_PATH = os.path.join(USER_DATA_DIR, "Default", "Network", "Cookies")
OUTPUT_FILE = os.path.expanduser(r"~\.notebooklm_extracted_cookies.json")

def get_secret_key():
    if not os.path.exists(LOCAL_STATE_PATH):
        return None
    with open(LOCAL_STATE_PATH, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:] # Remove DPAPI prefix
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_payload(cipher, payload):
    try:
        nonce = payload[3:15]
        ciphertext = payload[15:]
        return AESGCM(cipher).decrypt(nonce, ciphertext, None).decode('utf-8')
    except Exception:
        try:
            return win32crypt.CryptUnprotectData(payload, None, None, None, 0)[1].decode('utf-8')
        except Exception:
            return ""

def main():
    print("🔓 실행 중인 크롬의 세션 쿠키를 SQLite 직접 복호화로 추출합니다...")
    if not os.path.exists(COOKIES_PATH):
        print(f"❌ Cookies 파일 미발견: {COOKIES_PATH}")
        return

    key = get_secret_key()
    if not key:
        print("❌ 크롬 비밀키 복호화 실패")
        return

    temp_db = os.path.join(os.environ["TEMP"], "chrome_cookies_temp.db")
    shutil.copyfile(COOKIES_PATH, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc, is_secure, is_httponly FROM cookies WHERE host_key LIKE '%google%'")
    rows = cursor.fetchall()

    extracted_cookies = []
    for host, name, path, enc_val, exp, secure, httponly in rows:
        val = decrypt_payload(key, enc_val)
        if val and any(k in name for k in ["SID", "SAPISID", "APISID", "HSID", "SSID", "1PAPISID", "3PAPISID", "OSID"]):
            extracted_cookies.append({
                "domain": host,
                "name": name,
                "value": val,
                "path": path,
                "secure": bool(secure),
                "httpOnly": bool(httponly)
            })

    conn.close()
    if os.path.exists(temp_db):
        os.remove(temp_db)

    print(f"🔑 복호화된 구글 핵심 세션 쿠키: {len(extracted_cookies)}개")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(extracted_cookies, f, indent=2)

    print(f"💾 {OUTPUT_FILE} 저장 완료!")

if __name__ == "__main__":
    main()
