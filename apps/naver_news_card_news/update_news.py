import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import ssl
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from api_quota_guard import check_and_increment_quota

# .env 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path)

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

ssl_context = ssl._create_unverified_context()

# 8대 핵심 카테고리
CATEGORIES = [
    {"name": "엔터", "query": "연예"},
    {"name": "스포츠", "query": "축구"},
    {"name": "정치", "query": "정부"},
    {"name": "경제", "query": "주식"},
    {"name": "사회", "query": "속보"},
    {"name": "생활/문화", "query": "트렌드"},
    {"name": "IT/과학", "query": "AI"},
    {"name": "세계", "query": "미국"}
]

# 자극적이고 안 보면 안 될 것 같은 후킹 카피 변환 함수 (Loss Avoidance $L$ 적용)
def generate_hook_title(category, original_title):
    # 특수문자 및 태그 제거
    clean_title = re.sub(r'<[^>]+>', '', original_title)
    clean_title = re.sub(r'\[.*?\]', '', clean_title).strip()
    
    hooks = [
        f"🚨 [긴급] 안 보면 100% 손해! {clean_title}",
        f"⚠️ 모르면 바로 뒤처집니다! {clean_title}",
        f"💥 지금 난리 난 {category} 이슈: {clean_title}",
        f"🔥 대중 반응 폭발! {clean_title} 극비 전말",
        f"📢 실시간 검색 1위! {clean_title} 경악"
    ]
    import random
    # 해시값을 기준으로 일관성 있게 후킹 타이틀 생성
    idx = abs(hash(clean_title)) % len(hooks)
    return hooks[idx]

def get_og_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        response = urllib.request.urlopen(req, context=ssl_context, timeout=4)
        html = response.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&q=80&w=1080"

def fetch_category_trending_news():
    results = []
    rank = 1
    
    for cat in CATEGORIES:
        # 일일 무료 한도 80% 안전 임계치 체크
        if not check_and_increment_quota(1):
            print(f"⚠️ {cat['name']} 카테고리는 무료 한도 초과 방지를 위해 수집을 건너땁니다.")
            continue
            
        query_str = cat['query']
        encoded_query = urllib.parse.quote(query_str)
        
        # 네이버 API HUB - 관련도/인기순 뉴스 조회
        url = f"https://naverapihub.apigw.ntruss.com/search/v1/news?query={encoded_query}&display=2&sort=sim&format=json"
        
        try:
            request = urllib.request.Request(url)
            request.add_header("X-NCP-APIGW-API-KEY-ID", NAVER_CLIENT_ID)
            request.add_header("X-NCP-APIGW-API-KEY", NAVER_CLIENT_SECRET)
            
            response = urllib.request.urlopen(request, context=ssl_context)
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                items = data.get('items', [])
                
                for item in items:
                    raw_title = item['title']
                    clean_title = re.sub(r'<[^>]+>', '', raw_title)
                    hook_title = generate_hook_title(cat['name'], clean_title)
                    
                    link = item['originallink'] if item.get('originallink') else item['link']
                    image_url = get_og_image(link)
                    
                    results.append({
                        "rank": rank,
                        "category": cat['name'],
                        "raw_title": clean_title,
                        "hook_title": hook_title,
                        "source": "네이버 인기 뉴스",
                        "link": link,
                        "image_url": image_url
                    })
                    rank += 1
        except Exception as e:
            print(f"Error fetching {cat['name']}: {e}")
            
    return results

if __name__ == "__main__":
    print("전 분야 (엔터, 스포츠, 정치, 경제, 사회, 생활, IT, 세계) 핫뉴스 수집 중...")
    news_data = fetch_category_trending_news()
    
    out_file = os.path.join(os.path.dirname(__file__), "top10_news_data.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
        
    print(f"수집 완료: 총 {len(news_data)}개 수집됨")
