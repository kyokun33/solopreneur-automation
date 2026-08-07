import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_persistent_session")
COOKIE_FILE = os.path.expanduser(r"~\.notebooklm_extracted_cookies.json")

async def extract():
    print("🍪 구글 전체 인증 세션 쿠키(SID, SAPISID 등)를 수집합니다...")
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=True
            )
        except Exception:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=True
            )

        page = context.pages[0] if context.pages else await context.new_page()
        print("🌐 https://notebooklm.google.com/ 으로 이동...")
        await page.goto("https://notebooklm.google.com/", wait_until="networkidle")
        await asyncio.sleep(2)

        cookies = await context.cookies()
        print(f"✅ 총 {len(cookies)}개 구글 전체 쿠키 수집 완료!")

        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)

        print(f"💾 쿠키 저장 파일: {COOKIE_FILE}")

if __name__ == "__main__":
    asyncio.run(extract())
