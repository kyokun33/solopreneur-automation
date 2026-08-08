import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_log_project_final_complete.png"

async def run():
    print("✏️ 상단 노트북 제목을 '로그 프로젝트'로 최종 정교화 치환합니다...")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            no_viewport=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.bring_to_front()
        
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. 메인 대문에 '제목 없는 노트북' 카드가 있으면 진입
        untitled_card = page.get_by_text("제목 없는 노트북").first
        if await untitled_card.count() > 0 and await untitled_card.is_visible():
            await untitled_card.click(force=True)
            await asyncio.sleep(3.5)

        # 2. 내부 화면 상단 제목 '제목 없는 노트북' 치환
        title_btn = page.locator("text='제목 없는 노트북'").first
        if await title_btn.count() > 0 and await title_btn.is_visible():
            await title_btn.click(force=True)
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type("로그 프로젝트", delay=80)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2.5)

        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print("🎉 제목까지 '로그 프로젝트'로 최종 완료!")
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
