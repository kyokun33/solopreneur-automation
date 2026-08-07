import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CHROME_USER_DATA = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
COOKIE_FILE = os.path.expanduser(r"~\.notebooklm_extracted_cookies.json")

async def extract():
    print("🍪 대표님의 실제 크롬 기본 프로필(User Data)에서 구글 로그인 세션 쿠키를 직접 추출합니다...")
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=CHROME_USER_DATA,
                channel="chrome",
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = context.pages[0] if context.pages else await context.new_page()
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            await asyncio.sleep(2)

            cookies = await context.cookies()
            print(f"✅ 대표님 실제 크롬 프로필에서 총 {len(cookies)}개 세션 쿠키 추출 성공!")

            with open(COOKIE_FILE, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)

            print(f"💾 쿠키 저장 완료: {COOKIE_FILE}")
            await context.close()
        except Exception as e:
            print(f"⚠️ 대표님 프로필 직접 추출 예외 (크롬 실행 중일 수 있음): {e}")

if __name__ == "__main__":
    asyncio.run(extract())
