import json
import os
import random
import string
import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(ROOT_DIR, "report_generator", "keys.json")
OUTPUT_TXT = os.path.join(ROOT_DIR, "kmong_serial_keys_list.txt")

def generate_random_key(prefix="KMONG"):
    rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{rand_part[:4]}-{rand_part[4:]}"

def create_bulk_keys(count=20):
    existing_keys = {}
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                existing_keys = json.load(f)
        except Exception:
            existing_keys = {}

    new_keys_list = []
    for _ in range(count):
        k = generate_random_key()
        while k in existing_keys:
            k = generate_random_key()
        existing_keys[k] = {
            "used": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        new_keys_list.append(k)

    os.makedirs(os.path.dirname(KEYS_FILE), exist_ok=True)
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_keys, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("==========================================\n")
        f.write("🔑 크몽 결제 무인 전달용 1회용 시리얼 코드 리스트\n")
        f.write("==========================================\n\n")
        for idx, k in enumerate(new_keys_list, 1):
            f.write(f"[{idx:02d}] {k}\n")

    print(f"[SUCCESS] {count}개의 1회용 시리얼 키 생성 완료!")
    print(f" -> DB 업데이트: {KEYS_FILE}")
    print(f" -> 텍스트 리스트 저장: {OUTPUT_TXT}")

if __name__ == "__main__":
    create_bulk_keys(20)
