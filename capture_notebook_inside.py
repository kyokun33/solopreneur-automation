import asyncio
import os
import sys
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"
INSIDE_SHOT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_inside_result.png"

async def run():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            page = context.pages[0]
            await page.bring_to_front()
            
            # '로그 프로젝트' 노트북 카드 클릭
            card = page.get_by_text("로그 프로젝트").first
            if await card.count() > 0:
                await card.click(force=True)
                await asyncio.sleep(4)
                
            await page.screenshot(path=INSIDE_SHOT, full_page=True)
            print(f"📸 노트북 내부 스크린샷 저장 완료: {INSIDE_SHOT}")
        except Exception as e:
            print(f"오류: {e}")

if __name__ == "__main__":
    asyncio.run(run())
