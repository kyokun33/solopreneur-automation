import asyncio
import os
from playwright.async_api import async_playwright

PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"

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
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Create new notebook
        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            await new_btn.click()
            await asyncio.sleep(4)

        print("Current URL:", page.url)

        # Click '복사한 텍스트'
        print("Clicking '복사한 텍스트' element...")
        copied_text_btn = page.locator("div, button, span").filter(has_text="복사한 텍스트").last
        await copied_text_btn.click(force=True)
        await asyncio.sleep(3)

        await page.screenshot(path="temp_modal_after_click_copied.png", full_page=True)

        # Check for textarea / input / buttons in the paste modal
        textareas = page.locator("textarea, [contenteditable='true']")
        print(f"Textareas count: {await textareas.count()}")
        if await textareas.count() > 0:
            print("Typing sample text into textarea...")
            await textareas.first.fill("샘플 프로젝트 테스트 본문입니다.")
            await asyncio.sleep(1)

        # Check insert button
        insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert')").first
        print(f"Insert button count: {await insert_btn.count()}")
        if await insert_btn.count() > 0:
            print("Clicking insert button...")
            await insert_btn.click(force=True)
            await asyncio.sleep(6)

        await page.screenshot(path="temp_modal_after_insert.png", full_page=True)

        # Check if source appears in left panel!
        sources = await page.locator("div[role='listitem'], div[class*='source']").all_inner_texts()
        print("Sources in panel:", sources[:10])

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
