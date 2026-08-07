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
PRIMARY_COOKIES_DB = os.path.join(USER_DATA_DIR, "Default", "Network", "Cookies")

def get_secret_key():
    if not os.path.exists(LOCAL_STATE_PATH):
        return None
    with open(LOCAL_STATE_PATH, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:] # DPAPI prefix 제거
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_payload(cipher, payload):
    try:
        if payload.startswith(b'v10') or payload.startswith(b'v11'):
            nonce = payload[3:15]
            ciphertext = payload[15:]
            return AESGCM(cipher).decrypt(nonce, ciphertext, None).decode('utf-8', errors='ignore')
        else:
            return win32crypt.CryptUnprotectData(payload, None, None, None, 0)[1].decode('utf-8', errors='ignore')
    except Exception:
        return ""

def get_user_google_cookies():
    key = get_secret_key()
    if not key:
        print("❌ 복호화 비밀키 미발견")
        return []

    if not os.path.exists(PRIMARY_COOKIES_DB):
        print(f"❌ 크롬 세션 DB 미발견: {PRIMARY_COOKIES_DB}")
        return []

    temp_db = os.path.join(os.environ["TEMP"], "real_user_chrome_cookies.db")
    shutil.copyfile(PRIMARY_COOKIES_DB, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc, is_secure, is_httponly FROM cookies WHERE host_key LIKE '%google.com%'")
    rows = cursor.fetchall()

    cookies_list = []
    for host, name, path, enc_val, exp, secure, httponly in rows:
        val = decrypt_payload(key, enc_val)
        if val:
            domain = host if host.startswith(".") else f".{host.lstrip('.')}"
            cookies_list.append({
                "name": name,
                "value": val,
                "domain": domain,
                "path": path,
                "secure": bool(secure),
                "httpOnly": bool(httponly),
                "sameSite": "Lax"
            })

    conn.close()
    if os.path.exists(temp_db):
        os.remove(temp_db)

    print(f"🔑 대표님의 Chrome 실제 구글 복호화 쿠키: {len(cookies_list)}개 발견!")
    return cookies_list

if __name__ == "__main__":
    c_list = get_user_google_cookies()
    print("대표 구글 쿠키 수집 완수:", len(c_list))
