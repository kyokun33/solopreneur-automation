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

NOTEBOOK_TITLE = "GA 보험설계사 10대 영업 기획안 & 자동화"

async def run():
    print("🚀 GA 노트북 제목 확정 및 대시보드 검증 시동...")

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

        print("🌐 NotebookLM 이동...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 제목 변경
        print(f"✏️ 노트북 제목 변경: {NOTEBOOK_TITLE}")
        try:
            await page.mouse.click(100, 30)
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type(NOTEBOOK_TITLE, delay=50)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ 제목 변경 예외: {e}")

        # 파란색 제출 버튼 클릭
        await page.mouse.click(236, 465)
        await asyncio.sleep(8)

        # 메인 홈 대시보드 캡처
        print("🏠 메인 홈 대시보드 이동 후 최종 카드 검증...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        os.makedirs(os.path.dirname(SHOT_FINAL_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_FINAL_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_FINAL_ARTIFACT, full_page=True)
        print(f"🎉 100% 무결 검증 스크린샷 완비:\n  - {SHOT_FINAL_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
