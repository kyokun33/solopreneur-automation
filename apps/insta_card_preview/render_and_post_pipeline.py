import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("🚀 [1인기업 무인 자동화] 인스타그램 4컷 웹툰 및 8대 분야 뉴스 렌더링 파이프라인 정비")

# Paths
base_dir = r"f:\1인기업\apps\insta_card_preview"
html_template = os.path.join(base_dir, "zzansik_webtoon_template.html")
out_dir = r"C:\Users\sude3\OneDrive\바탕 화면"

def render_html_to_image(html_path, output_jpg_path):
    """HTML 템플릿을 고화질 1080x1350 JPEG 이미지로 렌더링"""
    if not os.path.exists(html_path):
        print(f"❌ HTML 파일 없음: {html_path}")
        return False

    file_url = f"file:///{os.path.abspath(html_path).replace('\\', '/')}"
    print(f"📸 Playwright 렌더링 시작: {file_url}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1080, "height": 1350})
            page.goto(file_url, wait_until="load")
            time.sleep(1) # Font & styling settle
            page.screenshot(path=output_jpg_path, type="jpeg", quality=95)
            browser.close()
        print(f"✅ 렌더링 성공! 이미지 저장: {output_jpg_path}")
        return True
    except Exception as e:
        print(f"❌ 렌더링 실패: {e}")
        return False

if __name__ == "__main__":
    out_img = os.path.join(out_dir, "짠식이네_4컷웹툰_EP1_템플릿.jpg")
    success = render_html_to_image(html_template, out_img)
    if success:
        print("🎉 [준비 완료] 저녁 7시 24분 AI 한도 해제 후 4컷 만화컷 생성 및 조합이 100% 자동 실행됩니다.")
