import requests
from bs4 import BeautifulSoup
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_naver_top_news():
    url = 'https://news.naver.com/main/ranking/popularDay.naver'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    boxes = soup.select('.rankingnews_box')
    results = []
    
    for box in boxes:
        press_name = box.select_one('.rankingnews_name')
        press = press_name.text.strip() if press_name else "주요언론"
        
        list_items = box.select('.rankingnews_list li')
        for item in list_items:
            title_tag = item.select_one('a.list_title')
            img_tag = item.select_one('img')
            
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag['href']
                img_url = ''
                if img_tag:
                    img_url = img_tag.get('src') or img_tag.get('data-src') or ''
                
                results.append({
                    'press': press,
                    'title': title,
                    'link': link,
                    'img_url': img_url
                })
                
    # Filter top 5 distinct news items from different presses if possible
    top5 = []
    seen_titles = set()
    for n in results:
        if n['title'] not in seen_titles and len(top5) < 5:
            seen_titles.add(n['title'])
            top5.append(n)
            
    print(f"Fetched {len(top5)} news articles from Naver:")
    for i, n in enumerate(top5, 1):
        print(f"{i}. [{n['press']}] {n['title']}")
        print(f"   Image: {n['img_url']}")
        
    with open('naver_top5.json', 'w', encoding='utf-8') as f:
        json.dump(top5, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    fetch_naver_top_news()
