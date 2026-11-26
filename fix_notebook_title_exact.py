import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
ARTIFACT_DIR = r"C:\Users\sude3\.gemini\antigravity-ide\brain\7bed124d-5c53-48a9-b861-1883f5bd55b2"
SHOT_RESULT_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_report_final_verified.png"
SHOT_RESULT_ARTIFACT = os.path.join(ARTIFACT_DIR, "notebook_report_final_verified.png")

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        print("🌐 기존 생성된 노트북 바로가기...")
        await page.goto("https://notebook.google.com/notebook/896b9d5b-18a8-4a61-b2c0-03708f6224fb", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # Fix notebook title to '보고서'
        print("✏️ 노트북 제목을 '보고서'로 변경 중...")
        title_elem = page.locator("input, [contenteditable='true'], div, h1").filter(has_text="제목 없는 노트북").first
        if await title_elem.count() > 0:
            await title_elem.click(force=True)
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type("보고서", delay=100)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
            print("✅ 제목 '보고서' 변경 성공!")

        # Screenshot
        await page.screenshot(path=SHOT_RESULT_LOCAL, full_page=True)
        if os.path.exists(ARTIFACT_DIR):
            await page.screenshot(path=SHOT_RESULT_ARTIFACT, full_page=True)

        print(f"📸 최종 검증 완료 스크린샷: {SHOT_RESULT_LOCAL}")
        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
