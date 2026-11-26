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
    print("🧹 대시보드 내 소스 0개 빈 노트북 정리 삭제 시동...")

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

        print("🌐 NotebookLM 메인 이동...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 소스 0개 카드들 3점 버튼 클릭 후 삭제
        for i in range(5):
            try:
                card_0 = page.locator("mat-card:has-text('소스 0개'), div:has-text('소스 0개')").first
                if await card_0.count() > 0:
                    dots = card_0.locator("button, [aria-label*='옵션'], [aria-label*='메뉴'], mat-icon:has-text('more_vert')").first
                    if await dots.count() > 0:
                        await dots.click(force=True)
                        await asyncio.sleep(1)
                        del_btn = page.get_by_text("삭제").first
                        if await del_btn.count() > 0:
                            await del_btn.click(force=True)
                            await asyncio.sleep(1)
                            confirm_btn = page.locator("button:has-text('삭제'), button:has-text('확인')").last
                            if await confirm_btn.count() > 0:
                                await confirm_btn.click(force=True)
                                await asyncio.sleep(2)
                                print(f"🗑️ 소스 0개 빈 카드 {i+1}번 삭제 완료!")
            except Exception as e:
                print(f"⚠️ 삭제 패스: {e}")
                break

        print("🏠 클린 대시보드 최종 스크린샷 저장...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        os.makedirs(os.path.dirname(SHOT_FINAL_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_FINAL_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_FINAL_ARTIFACT, full_page=True)
        print(f"🎉 정리 완료 대시보드 스크린샷 완비:\n  - {SHOT_FINAL_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
