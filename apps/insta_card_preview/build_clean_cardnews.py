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

# Purge existing files
for f in os.listdir(OUTPUT_DIR):
    if f.endswith(('.jpg', '.png', '.jpeg', '.txt')):
        try:
            os.remove(os.path.join(OUTPUT_DIR, f))
        except Exception:
            pass

# 100% Commercially Royalty-Free High-Res Unsplash Images
CLEAN_IMAGES = {
    'cover': 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1080&auto=format&fit=crop',
    'news1': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&auto=format&fit=crop',
    'news2': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1080&auto=format&fit=crop',
    'news3': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1080&auto=format&fit=crop',
    'news4': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1080&auto=format&fit=crop',
    'news5': 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=1080&auto=format&fit=crop',
    'outro': 'https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=1080&auto=format&fit=crop'
}

# 100% Paraphrased original titles & descriptions
CLEAN_NEWS = [
    {
        'title': "중국 반도체 치킨게임 결국 항복 선언! 반사 이익 노리는 국내 기업들",
        'sub': "글로벌 메모리 반도체 공급 과잉 해소 전망... 국내 반도체 업계 호재 가능성 집중 분석",
        'link': "https://n.news.naver.com/mnews/article/015/0005327706",
        'img': CLEAN_IMAGES['news1']
    },
    {
        'title': "용혜인 의원 앞머리 '흰 줄' 정체 공개... 용기 있는 고백에 관심 응원 폭증",
        'sub': "헤어 브릿지가 아닌 백반증 질환 고백... 정치권 및 네티즌들의 격려 물결 이어져",
        'link': "https://n.news.naver.com/mnews/article/015/0005327807",
        'img': CLEAN_IMAGES['news2']
    },
    {
        'title': "지방 거점 국립대 연 1000억 파격 지원! 대학 입시 판도 대격변 예고",
        'sub': "정부의 '지역 거점대 집중 육성' 사업 첫 타자 선정... 부산대 등 대규모 예산 투입 확정",
        'link': "https://n.news.naver.com/mnews/article/015/0005327840",
        'img': CLEAN_IMAGES['news3']
    },
    {
        'title': "국민연금 신뢰도 논란 속 세대별 개편안 격돌... 고갈 시기 전망 재조명",
        'sub': "젊은 층의 연금 불신과 수령액 개편 논란 본격화... 향후 국가 연금 제도 재정비 과제",
        'link': "https://n.news.naver.com/mnews/article/015/0005327829",
        'img': CLEAN_IMAGES['news4']
    },
    {
        'title': "BTS 뷔도 착용한 78만 원짜리 '스마트 반도'? 차세대 헬스케어 링 돌풍",
        'sub': "수면 측정과 건강 관리가 손가락 하나로... 전 세계적인 트렌드로 부상한 웨어러블 반도 기기",
        'link': "https://n.news.naver.com/mnews/article/015/0005327862",
        'img': CLEAN_IMAGES['news5']
    }
]

def generate_html_card(slide_type, data=None, num=0):
    if slide_type == 'cover':
        title_html = "🔥 오늘자 실시간 핫이슈 TOP 5"
        sub_html = "오늘 대한민국에서 가장 뜨거운 5가지 트렌드를 한눈에!"
        img_src = CLEAN_IMAGES['cover']
        tag = "실시간 핫이슈"
    elif slide_type == 'outro':
        title_html = "📢 기사 원문이 궁금하다면?"
        sub_html = "댓글에 '뉴스'라고 남겨주시면 원문 링크 5개를 DM으로 쏴드립니다! 💌"
        img_src = CLEAN_IMAGES['outro']
        tag = "원문 링크 받기"
    else:
        title_html = data['title']
        sub_html = data['sub']
        img_src = data['img']
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
        padding: 8px 22px;
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
        font-size: 40px;
        font-weight: 900;
        line-height: 1.45;
        word-break: keep-all;
        letter-spacing: -1px;
    }}
    .news-sub {{
        color: #94a3b8;
        font-size: 25px;
        font-weight: 700;
        line-height: 1.5;
        margin-top: 22px;
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
        <img src="{img_src}" class="main-img" alt="뉴스 이미지">
        <div class="tag-badge">{tag}</div>
    </div>
    <div class="content-container">
        <div>
            <div class="news-title">{title_html}</div>
            <div class="news-sub">{sub_html}</div>
        </div>
        <div class="footer-bar">
            <div class="brand-logo">⚡ 오늘자 핫이슈 요약 TOP 5</div>
            <div class="slide-num">{num if slide_type=='news' else ('START' if slide_type=='cover' else 'END')} / 5</div>
        </div>
    </div>
</body>
</html>"""
    return html

def main():
    print("🛡️ 바이럴 댓글 유도형(DM 발송) 클린 카드뉴스 파이프라인 가동...")
    
    html_files = []
    
    # 1. Cover
    cover_html = generate_html_card('cover')
    with open('slide_0_cover.html', 'w', encoding='utf-8') as f:
        f.write(cover_html)
    html_files.append(('slide_0_cover.html', '01_클린핫이슈_표지.jpg'))
    
    # 2. News 1~5
    news_titles_summary = []
    for idx, item in enumerate(CLEAN_NEWS, 1):
        filename = f'slide_{idx}_news.html'
        out_jpg = f'{idx:02d}_클린핫이슈_뉴스{idx}.jpg'
        card_html = generate_html_card('news', item, num=idx)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(card_html)
        html_files.append((filename, out_jpg))
        
        news_titles_summary.append(f"{idx}위. {item['title']}")
        
    # 3. Outro (DM Trigger Focus)
    outro_html = generate_html_card('outro')
    with open('slide_6_outro.html', 'w', encoding='utf-8') as f:
        f.write(outro_html)
    html_files.append(('slide_6_outro.html', '07_클린핫이슈_아웃트로.jpg'))

    # Generate Viral Caption File (No URLs in caption! Comment DM Trigger!)
    caption_text = f"""🔥 오늘자 실시간 핫이슈 TOP 5 한눈에 보기!

오늘 대한민국에서 가장 뜨거운 관심사 5가지를 요약했습니다.

----------------------------------------
{chr(10).join(news_titles_summary)}
----------------------------------------

💬 5가지 뉴스의 상세 기사 원문이 궁금하신가요?
아래 댓글창에 ['뉴스']라고 남겨주시면, 원문 링크 5개를 DM으로 즉시 발송해 드립니다! 💌

❤️ 매일 실시간 핫이슈를 가장 빠르게 알고 싶다면 '팔로우' 부탁드립니다!
#오늘의뉴스 #실시간핫이슈 #트렌드요약 #뉴스카드뉴스 #핫이슈 #오늘의이슈 #이슈뉴스
"""
    caption_path = os.path.join(OUTPUT_DIR, "인스타그램_포스팅_캡션 및 원문링크.txt")
    with open(caption_path, 'w', encoding='utf-8') as f:
        f.write(caption_text)

    # Render via Playwright
    print("📸 Playwright 1080x1350 바이럴 카드뉴스 렌더링...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for html_f, out_jpg in html_files:
            page = browser.new_page(viewport={"width": 1080, "height": 1350})
            abs_path = os.path.abspath(html_f).replace('\\', '/')
            page.goto(f"file:///{abs_path}", wait_until="networkidle")
            page.wait_for_timeout(1000)
            
            save_path = os.path.join(OUTPUT_DIR, out_jpg)
            page.screenshot(path=save_path, type="jpeg", quality=95, full_page=True)
            print(f"  ✅ Viral Card Saved: {out_jpg}")
        browser.close()

    print("\n🎉 바이럴 댓글 유도형 무결점 카드뉴스 생성 완료!")

if __name__ == '__main__':
    main()
