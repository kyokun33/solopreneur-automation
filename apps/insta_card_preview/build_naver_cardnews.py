import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Output directory for desktop
OUTPUT_DIR = r"C:\Users\sude3\OneDrive\바탕 화면\인스타그램_카드뉴스_오늘자핫이슈"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Purge existing images in output dir
for f in os.listdir(OUTPUT_DIR):
    if f.endswith(('.jpg', '.png', '.jpeg', '.txt')):
        try:
            os.remove(os.path.join(OUTPUT_DIR, f))
        except Exception:
            pass

def get_high_res_img(img_url):
    if not img_url:
        return "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=1080&auto=format&fit=crop"
    if 'type=nf70_70' in img_url:
        return img_url.replace('type=nf70_70', 'type=w800')
    elif '?' in img_url:
        return img_url.split('?')[0] + '?type=w800'
    return img_url

def fetch_top5_news():
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
                    'img_url': get_high_res_img(img_url)
                })
                
    top5 = []
    seen = set()
    for n in results:
        if n['title'] not in seen and len(top5) < 5:
            seen.add(n['title'])
            top5.append(n)
            
    return top5

def generate_html_card(slide_type, data, num=0):
    """
    1080x1350 Cardnews without 'Naver' branding.
    """
    if slide_type == 'cover':
        title_html = "🔥 오늘자 실시간 핫이슈 TOP 5"
        sub_html = "오늘 대한민국에서 가장 관심 폭발한 뉴스 5가지를 한눈에!"
        img_src = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1080&auto=format&fit=crop"
        tag = "실시간 핫이슈"
    elif slide_type == 'outro':
        title_html = "📢 매일 매일 업데이트되는 핫이슈!"
        sub_html = "팔로우 & 좋아요 누르고 내일 뉴스도 빠르게 받아보세요 ❤️"
        img_src = "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=1080&auto=format&fit=crop"
        tag = "뉴스 구독하기"
    else:
        title_html = f"[{data['press']}] {data['title']}"
        sub_html = f"오늘 가장 높은 관심도를 기록한 뉴스 {num}위"
        img_src = data['img_url']
        tag = f"TOP {num}"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, height=1350, initial-scale=1.0">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@700;900&display=swap');
    
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        width: 1080px;
        height: 1350px;
        background-color: #0b0f19;
        font-family: 'Gothic A1', sans-serif;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }}
    .image-container {{
        width: 1080px;
        height: 675px;
        position: relative;
        background-color: #1e293b;
        overflow: hidden;
    }}
    .main-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    .tag-badge {{
        position: absolute;
        top: 30px;
        left: 30px;
        background-color: #ff0055;
        color: #ffffff;
        font-size: 24px;
        font-weight: 900;
        padding: 8px 20px;
        border-radius: 30px;
        border: 3px solid #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
    .content-container {{
        width: 1080px;
        height: 675px;
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        padding: 50px 60px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border-top: 6px solid #ff0055;
    }}
    .news-title {{
        color: #ffffff;
        font-size: 42px;
        font-weight: 900;
        line-height: 1.45;
        word-break: keep-all;
        letter-spacing: -1px;
    }}
    .news-sub {{
        color: #94a3b8;
        font-size: 26px;
        font-weight: 700;
        line-height: 1.5;
        margin-top: 20px;
        word-break: keep-all;
    }}
    .footer-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 2px solid #1e293b;
        padding-top: 24px;
    }}
    .brand-logo {{
        color: #ffe600;
        font-size: 26px;
        font-weight: 900;
    }}
    .slide-num {{
        color: #64748b;
        font-size: 22px;
        font-weight: 900;
    }}
</style>
</head>
<body>
    <div class="image-container">
        <img src="{img_src}" class="main-img" alt="뉴스 이미지" onerror="this.src='https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=1080&auto=format&fit=crop'">
        <div class="tag-badge">{tag}</div>
    </div>
    <div class="content-container">
        <div>
            <div class="news-title">{title_html}</div>
            <div class="news-sub">{sub_html}</div>
        </div>
        <div class="footer-bar">
            <div class="brand-logo">⚡ 실시간 핫이슈 TOP 5</div>
            <div class="slide-num">{num if slide_type=='news' else ('START' if slide_type=='cover' else 'END')} / 5</div>
        </div>
    </div>
</body>
</html>"""
    return html

def main():
    print("📰 실시간 핫뉴스 TOP 5 데이터 수집 중...")
    news_items = fetch_top5_news()
    
    html_files = []
    
    # 1. Cover
    cover_html = generate_html_card('cover', None)
    with open('slide_0_cover.html', 'w', encoding='utf-8') as f:
        f.write(cover_html)
    html_files.append(('slide_0_cover.html', '01_핫이슈TOP5_표지.jpg'))
    
    # 2. News 1~5
    caption_links = []
    for idx, item in enumerate(news_items, 1):
        filename = f'slide_{idx}_news.html'
        out_jpg = f'{idx:02d}_핫이슈TOP5_뉴스{idx}.jpg'
        card_html = generate_html_card('news', item, num=idx)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(card_html)
        html_files.append((filename, out_jpg))
        
        caption_links.append(f"{idx}위. [{item['press']}] {item['title']}\n🔗 원문 링크: {item['link']}\n")
        
    # 3. Outro
    outro_html = generate_html_card('outro', None)
    with open('slide_6_outro.html', 'w', encoding='utf-8') as f:
        f.write(outro_html)
    html_files.append(('slide_6_outro.html', '07_핫이슈TOP5_아웃트로.jpg'))

    # Generate Instagram Caption File with Links
    caption_text = f"""🔥 오늘자 실시간 핫이슈 TOP 5 요약!

오늘 대한민국에서 가장 이슈가 되고 있는 뉴스 5가지를 한눈에 정리했습니다.
자세한 기사 원문이 궁금하신 분들은 아래 링크를 확인해 보세요! 👇

----------------------------------------
{chr(10).join(caption_links)}
----------------------------------------

❤️ 매일 핵심 뉴스를 빠르게 알고 싶다면 '팔로우' 부탁드립니다!
#오늘의뉴스 #실시간핫이슈 #뉴스요약 #카드뉴스 #이슈이슈 #오늘의이슈 #뉴스정보
"""
    caption_path = os.path.join(OUTPUT_DIR, "인스타그램_포스팅_캡션 및 원문링크.txt")
    with open(caption_path, 'w', encoding='utf-8') as f:
        f.write(caption_text)
    print(f"📝 캡션 및 원문 링크 파일 생성 완료: {caption_path}")

    # Render all slides via Playwright
    print("📸 1080x1350 초고화질 카드뉴스 렌더링 시작...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for html_f, out_jpg in html_files:
            page = browser.new_page(viewport={"width": 1080, "height": 1350})
            abs_path = os.path.abspath(html_f).replace('\\', '/')
            page.goto(f"file:///{abs_path}", wait_until="networkidle")
            page.wait_for_timeout(1000)
            
            save_path = os.path.join(OUTPUT_DIR, out_jpg)
            page.screenshot(path=save_path, type="jpeg", quality=95, full_page=True)
            print(f"  ✅ Saved: {out_jpg}")
        browser.close()

    print(f"\n🎉 '네이버' 표기를 완전히 제외한 깔끔한 실시간 핫이슈 카드뉴스 생성 완료!")

if __name__ == '__main__':
    main()
