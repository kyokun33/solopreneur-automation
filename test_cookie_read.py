import shutil
import os
import sqlite3

def dump_cookies():
    cookie_db = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies")
    temp_db = "temp_cookies.sqlite"
    
    try:
        # Try to copy the file directly
        shutil.copy2(cookie_db, temp_db)
        print("Copied successfully via shutil!")
    except Exception as e:
        print("Shutil copy failed:", e)
        # On Windows, if a file is locked, we might still be able to read it using Windows API or simply opening it read-only
        # Let's try to read it directly using URI
        print("Attempting to connect with URI read-only...")
        try:
            conn = sqlite3.connect(f"file:{cookie_db}?mode=ro", uri=True)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key LIKE '%google.com%'")
            print(f"Found {len(cursor.fetchall())} rows.")
            conn.close()
            print("Direct read successful!")
        except Exception as e2:
            print("Direct read failed:", e2)

if __name__ == "__main__":
    dump_cookies()
