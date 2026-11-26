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
SHOT_RESULT_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_cleaned_dashboard.png"
SHOT_RESULT_ARTIFACT = os.path.join(ARTIFACT_DIR, "notebook_cleaned_dashboard.png")

async def run():
    print("🧹 NotebookLM '제목 없는 노트북' 일괄 삭제 및 정리 작업 시동!")

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

        print("🌐 NotebookLM 메인 페이지 이동...")
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        deleted_count = 0

        while True:
            # Find cards with text '제목 없는 노트북'
            # Look for card elements that contain '제목 없는 노트북'
            untitled_cards = page.locator("div, article, mat-card").filter(has_text="제목 없는 노트북")
            count = await untitled_cards.count()
            print(f"🔍 탐지된 '제목 없는 노트북' 카드 수: {count}")

            if count == 0:
                print("✅ 모든 '제목 없는 노트북' 삭제 완료!")
                break

            # Process first card
            card = untitled_cards.first
            # Find 3 dots menu button inside or near the card
            more_btn = card.locator("button:has-text('more_vert'), button[aria-label*='옵션'], button[aria-label*='메뉴'], button[aria-label*='More'], button mat-icon:has-text('more_vert')").first
            if await more_btn.count() == 0:
                # Try finding icon inside card parent
                more_btn = card.locator("..").locator("button").filter(has_text="more_vert").first

            if await more_btn.count() > 0 and await more_btn.is_visible():
                print("⋮ 3점 메뉴 버튼 클릭...")
                await more_btn.click(force=True)
                await asyncio.sleep(1)

                # Look for '삭제' or 'Delete' menu item
                delete_item = page.locator("button, div, span").filter(has_text="삭제").first
                if await delete_item.count() > 0 and await delete_item.is_visible():
                    print("🗑️ '삭제' 메뉴 선택...")
                    await delete_item.click(force=True)
                    await asyncio.sleep(1.5)

                    # Look for confirmation dialog delete button
                    confirm_btn = page.locator("button:has-text('삭제'), button:has-text('확인'), button:has-text('Delete')").last
                    if await confirm_btn.count() > 0 and await confirm_btn.is_visible():
                        print("⚠️ 삭제 확인 버튼 클릭!")
                        await confirm_btn.click(force=True)
                        deleted_count += 1
                        print(f"🗑️ 총 {deleted_count}개 삭제 완료")
                        await asyncio.sleep(2)

                        # Check if also delete test notebook with 1 source if title is 'The Connect AI Automated Enterprise Test Source'
                        continue

            # If iteration couldn't click delete, break to avoid infinite loop
            print("⚠️ 삭제 메뉴 처리 불가, 대기 및 탈출...")
            break

        # Also check if there's any test notebook titled 'The Connect AI Automated Enterprise Test Source'
        test_cards = page.locator("div, article, mat-card").filter(has_text="The Connect AI Automated Enterprise Test Source")
        if await test_cards.count() > 0:
            print("🧹 추가 테스트 노트북 탐지, 삭제 진행...")
            card = test_cards.first
            more_btn = card.locator("button").filter(has_text="more_vert").first
            if await more_btn.count() > 0:
                await more_btn.click(force=True)
                await asyncio.sleep(1)
                del_btn = page.locator("button, div, span").filter(has_text="삭제").first
                if await del_btn.count() > 0:
                    await del_btn.click(force=True)
                    await asyncio.sleep(1.5)
                    confirm_btn = page.locator("button:has-text('삭제')").last
                    if await confirm_btn.count() > 0:
                        await confirm_btn.click(force=True)
                        await asyncio.sleep(2)

        # Final screenshot
        await page.screenshot(path=SHOT_RESULT_LOCAL, full_page=True)
        if os.path.exists(ARTIFACT_DIR):
            await page.screenshot(path=SHOT_RESULT_ARTIFACT, full_page=True)

        print(f"🎉 총 {deleted_count}개의 '제목 없는 노트북' 일괄 정리 완료!")
        print(f"📸 캡처 결과: {SHOT_RESULT_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())
