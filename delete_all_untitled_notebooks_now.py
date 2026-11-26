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
SHOT_RESULT_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_cleaned_dashboard_final.png"
SHOT_RESULT_ARTIFACT = os.path.join(ARTIFACT_DIR, "notebook_cleaned_dashboard_final.png")

async def run():
    print("🧹 NotebookLM '제목 없는 노트북' 일괄 삭제 파이프라인 시동...")

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

        print("🌐 NotebookLM 이동 및 대시보드 로딩 대기...")
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(5)

        deleted_count = 0

        for attempt in range(25):
            # Wait for cards to load fully
            await asyncio.sleep(2.5)

            # Find untitled cards
            untitled_cards = page.locator("div, article, mat-card").filter(has_text="제목 없는 노트북")
            count = await untitled_cards.count()

            test_cards = page.locator("div, article, mat-card").filter(has_text="The Connect AI Automated Enterprise Test Source")
            test_count = await test_cards.count()

            print(f"🔄 [시도 {attempt+1}] 미삭제 '제목 없는 노트북': {count}개 | 테스트 노치: {test_count}개")

            if count == 0 and test_count == 0:
                print("🎉 더 이상 삭제할 '제목 없는 노트북' 카드가 존재하지 않습니다!")
                break

            target = untitled_cards.first if count > 0 else test_cards.first

            # Find 3 dots button in this card
            more_btn = target.locator("button:has-text('more_vert')").first
            if await more_btn.count() == 0:
                more_btn = target.locator("..").locator("button:has-text('more_vert')").first

            if await more_btn.count() > 0 and await more_btn.is_visible():
                print(f"🎯 [{deleted_count+1}번째] 3점 메뉴 클릭...")
                await more_btn.click(force=True)
                await asyncio.sleep(1.2)

                del_item = page.get_by_text("삭제", exact=True)
                if await del_item.count() > 0:
                    box = await del_item.first.bounding_box()
                    if box:
                        await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        await asyncio.sleep(1.2)

                        confirm_btn = page.locator("mat-dialog-container button, div[role='dialog'] button").filter(has_text="삭제").first
                        if await confirm_btn.count() > 0 and await confirm_btn.is_visible():
                            await confirm_btn.click(force=True)
                            deleted_count += 1
                            print(f"✅ [{deleted_count}개 째] 삭제 완수! re-fetch 대기 (3.5초)...")
                            await asyncio.sleep(3.5)
                            continue

            # If failed to click, wait briefly and retry
            await asyncio.sleep(2)

        # Final wait for dashboard rendering
        print("⏳ 대시보드 최종 렌더링 대기 중 (5초)...")
        await asyncio.sleep(5)

        # Screenshot
        await page.screenshot(path=SHOT_RESULT_LOCAL, full_page=True)
        if os.path.exists(ARTIFACT_DIR):
            await page.screenshot(path=SHOT_RESULT_ARTIFACT, full_page=True)

        print(f"✨ 총 {deleted_count}개 '제목 없는 노트북' 일괄 완전 청소 성공!")
        print(f"📸 최종 스크린샷: {SHOT_RESULT_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
