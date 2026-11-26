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
    print("🚀 좌측 텍스트박스 포커스 및 Ctrl+Enter/블루버튼 직접 제출 시동...")

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

        # 1. 텍스트 박스 포커스 (x=100, y=250)
        print("🎯 텍스트박스 포커스 클릭 (100, 250)...")
        await page.mouse.click(100, 250)
        await asyncio.sleep(1)

        # 2. Ctrl+Enter 및 Enter 키 입력으로 제출 트리거!
        print("⌨️ Ctrl+Enter 제출 이벤트 전송...")
        await page.keyboard.press("Control+Enter")
        await asyncio.sleep(1)
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)

        # 3. 파란색 화살표 버튼 (236, 465) 클릭
        print("🔵 파란색 버튼 (236, 465) 클릭...")
        await page.mouse.click(236, 465)
        await asyncio.sleep(2)

        print("⏳ 소스 1개 파싱 및 인덱싱 처리 대기 (12초)...")
        await asyncio.sleep(12)

        # 4. 스크린샷 캡처
        os.makedirs(os.path.dirname(SHOT_FINAL_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_FINAL_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_FINAL_ARTIFACT, full_page=True)
        print(f"🎉 스크린샷 완비:\n  - {SHOT_FINAL_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
