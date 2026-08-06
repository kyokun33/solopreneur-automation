import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CDP_URL = "http://127.0.0.1:9222"
ARTIFACT_DIR = r"C:\Users\sude3\.gemini\antigravity-ide\brain\494e2ad8-498e-4bca-9b2f-d28dd07f2282"
SCREENSHOT_PATH = os.path.join(ARTIFACT_DIR, "notebook_inside_screen.png")

async def capture_inside():
    async with async_playwright() as p:
        try:
            print("NotebookLM 상세 페이지 접속 중...")
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            
            page = None
            for p_item in context.pages:
                if "notebooklm" in p_item.url:
                    page = p_item
                    break

            if page:
                await page.bring_to_front()
                # 최근 생성된 노트북 클릭
                notebook_card = page.locator("text=/AI Blueprint for Solo Venture Revenue|수익화 아이템|1인기업/")
                if await notebook_card.count() > 0:
                    print("생성된 노트북 카드 클릭 중...")
                    await notebook_card.first.click()
                    await asyncio.sleep(3)

                os.makedirs(ARTIFACT_DIR, exist_ok=True)
                await page.screenshot(path=SCREENSHOT_PATH, full_page=False)
                print(f"상세 스크린샷 캡처 완료: {SCREENSHOT_PATH}")

        except Exception as e:
            print(f"상세 스크린샷 오류: {e}")

if __name__ == "__main__":
    asyncio.run(capture_inside())
