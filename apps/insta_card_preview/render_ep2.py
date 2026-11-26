import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def render_html_to_jpeg():
    html_file = r"f:\1인기업\apps\insta_card_preview\ep2_webtoon.html"
    output_jpeg = r"C:\Users\sude3\OneDrive\바탕 화면\짠식이네_4컷웹툰_EP2_국가대표감독.jpg"
    
    file_url = f"file:///{html_file.replace('\\', '/')}"
    
    print(f"Playwright rendering started: {file_url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.screenshot(path=output_jpeg, type="jpeg", quality=95, full_page=True)
        
        browser.close()
        
    print(f"Rendering success: {output_jpeg}")

if __name__ == "__main__":
    render_html_to_jpeg()
