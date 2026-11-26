import json
import os
import sys
from datetime import datetime

# Windows encoding safety
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

QUOTA_FILE = os.path.join(os.path.dirname(__file__), "api_quota_tracker.json")
MAX_DAILY_QUOTA = 25000  # 네이버 검색 API 1일 무료 한도
SAFETY_THRESHOLD = 24250 # 97% 안전 임계치 (비용 발생 100% 방지)

def check_and_increment_quota(calls_count=1):
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    data = {"date": today_str, "used_today": 0}
    
    if os.path.exists(QUOTA_FILE):
        try:
            with open(QUOTA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("date") != today_str:
                    data = {"date": today_str, "used_today": 0}
        except Exception:
            data = {"date": today_str, "used_today": 0}
            
    if data["used_today"] + calls_count > SAFETY_THRESHOLD:
        print(f"[안전장치 발동] 오늘 사용량 ({data['used_today']}회)이 안전 한도 ({SAFETY_THRESHOLD}회)에 도달했습니다. 네이버 API 호출을 차단합니다.")
        return False
        
    data["used_today"] += calls_count
    
    with open(QUOTA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"[네이버 API 트래커] 오늘 총 {data['used_today']} / {MAX_DAILY_QUOTA} 회 사용중 (안전 구간 이내)")
    return True

if __name__ == "__main__":
    check_and_increment_quota(1)
