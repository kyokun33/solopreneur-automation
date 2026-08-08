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
    print("🚀 [고감독 영구 규칙 적용] 대표님 모니터 최상단 표출 & 작업 완료 후 새로고침 시동!")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--always-on-top"
            ],
            no_viewport=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.bring_to_front()

        print("🌐 NotebookLM 메인 대문 접속 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # '로그 프로젝트' 또는 노트북 진입
        log_card = page.get_by_text("로그 프로젝트").first
        if await log_card.count() > 0 and await log_card.is_visible():
            print("✨ '로그 프로젝트' 노트북 진입 중...")
            await log_card.click(force=True)
            await asyncio.sleep(3)

        # 대표님 지침: 작업 완료 후 자동 새로고침(Reload) 수행!
        print("🔄 [대표님 지침 준수] 최신 반영을 위해 새로고침(F5) 실행!")
        await page.reload(wait_until="domcontentloaded")
        await asyncio.sleep(3)

        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print("🎉 대표님 모니터 최상단 전면 표출 & 새로고침 완료!")

if __name__ == "__main__":
    asyncio.run(run())
