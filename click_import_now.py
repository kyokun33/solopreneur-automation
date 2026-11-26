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
ARTIFACT_DIR = r"C:\Users\sude3\.gemini\antigravity-ide\brain\7b4f8bfc-3d0c-4649-9cc2-2821ea88ace0"
SHOT_FINAL_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ga_insurance_notebook_FINAL_VERIFIED.png"
SHOT_FINAL_ARTIFACT = os.path.join(ARTIFACT_DIR, "ga_insurance_notebook_FINAL_VERIFIED.png")

async def run():
    print("🚀 NotebookLM '+ 가져오기' 버튼 클릭 시동...")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            no_viewport=True
        )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.bring_to_front()

        print("🌐 NotebookLM 접속...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. '+ 새 노트' 또는 기존 노트 클릭
        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            await new_btn.click()
            await asyncio.sleep(4)

        await page.keyboard.press("Escape")
        await asyncio.sleep(1)

        # 2. '+ 가져오기' 파란색 버튼 클릭!
        print("🔵 '+ 가져오기' 버튼 클릭 시도...")
        import_btn = page.locator("button:has-text('가져오기'), [aria-label*='가져오기']").first
        if await import_btn.count() > 0 and await import_btn.is_visible():
            await import_btn.click(force=True)
            print("✅ '+ 가져오기' 버튼 클릭 성공!")
        else:
            print("🔵 좌표 (214, 710) 직접 클릭...")
            await page.mouse.click(214, 710)

        print("⏳ 소스 인덱싱 및 AI 가공 처리 대기 (10초)...")
        await asyncio.sleep(10)

        # 3. 스튜디오 '보고서' 버튼 클릭
        try:
            report_btn = page.get_by_text("보고서").first
            if await report_btn.count() > 0 and await report_btn.is_visible():
                await report_btn.click(force=True)
                await asyncio.sleep(5)
        except Exception:
            pass

        # 4. 스크린샷 캡처
        os.makedirs(os.path.dirname(SHOT_FINAL_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_FINAL_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_FINAL_ARTIFACT, full_page=True)
        print(f"🎉 가져오기 완료 및 캡처 완비:\n  - {SHOT_FINAL_LOCAL}")

        await asyncio.sleep(3)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
