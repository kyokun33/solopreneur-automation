import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_log_project_final_complete.png"

async def run():
    print("🚀 모달 소스 주입 및 제목 변경 최종 타격...")
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

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
        await asyncio.sleep(3.5)

        # 1. 새 노트 만들기 클릭 (혹은 모달이 안열려있을 때)
        copied_tab = page.get_by_text("복사한 텍스트").first
        if not (await copied_tab.count() > 0 and await copied_tab.is_visible()):
            new_btn = page.get_by_text("새 노트 만들기").first
            if await new_btn.count() > 0 and await new_btn.is_visible():
                await new_btn.click(force=True)
                await asyncio.sleep(2.5)

        # 2. '복사한 텍스트' 클릭
        copied_tab = page.get_by_text("복사한 텍스트").first
        if await copied_tab.count() > 0 and await copied_tab.is_visible():
            print("📝 '복사한 텍스트' 클릭!")
            await copied_tab.click(force=True)
            await asyncio.sleep(1.5)

        # 3. 텍스트 채우기
        textarea = page.locator("textarea").first
        if await textarea.count() > 0 and await textarea.is_visible():
            print("✍️ 원고 100% 채우는 중...")
            await textarea.click(force=True)
            await textarea.fill(content_text)
            await asyncio.sleep(1.5)

            insert_btn = page.get_by_text("삽입").first
            if await insert_btn.count() > 0 and await insert_btn.is_visible():
                print("💾 '삽입' 타격 완료! AI 인덱싱 대기...")
                await insert_btn.click(force=True)
                await asyncio.sleep(7)

        # 4. 제목 치환
        print("✏️ 상단 타이틀 '로그 프로젝트' 치환 중...")
        title_btn = page.get_by_text("제목 없는 노트북").first
        if await title_btn.count() > 0 and await title_btn.is_visible():
            await title_btn.click(force=True)
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type("로그 프로젝트", delay=80)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)

        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print("🎉 [로그 프로젝트] 최종 완수 완료!")
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
