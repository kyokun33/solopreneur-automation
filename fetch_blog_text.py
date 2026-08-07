import asyncio
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def fetch_blog():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("🌐 네이버 블로그 포스트 페이지 방문 중...")
        await page.goto("https://blog.naver.com/procpalee/224188840058", wait_until="networkidle")
        
        # iframe(mainFrame) 파싱
        frame = page.frame(name="mainFrame")
        if frame:
            text = await frame.inner_text("body")
            print("=== 네이버 블로그 본문 텍스트 ===")
            print(text[:3000])
            with open("naver_blog_content.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("💾 naver_blog_content.txt 저장 완료!")
        else:
            text = await page.inner_text("body")
            print(text[:2000])
        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_blog())
