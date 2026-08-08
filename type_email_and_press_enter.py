import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def run():
    print("🚀 대표님 이메일 sude3333333@gmail.com 정밀 타이핑 및 Enter 가동...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            await page.bring_to_front()
            
            email_box = page.locator("input[type='email'], input[name='identifier']").first
            if await email_box.count() > 0 and await email_box.is_visible():
                await email_box.click(force=True)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type("sude3333333@gmail.com", delay=70)
                await asyncio.sleep(0.8)
                await page.keyboard.press("Enter")
                print("✅ sude3333333@gmail.com 입력 및 Enter 완료!")
            else:
                print("⚠️ 이메일 입력창 미발견")
        except Exception as e:
            print(f"예외: {e}")

if __name__ == "__main__":
    asyncio.run(run())
