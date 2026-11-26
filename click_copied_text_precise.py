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

        # Find exact text element '복사된 텍스트'
        elem = page.get_by_text("복사된 텍스트", exact=True)
        print("get_by_text count:", await elem.count())

        if await elem.count() > 0:
            box = await elem.first.bounding_box()
            print("Bounding box:", box)
            if box:
                await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                await asyncio.sleep(3)

        await page.screenshot(path="temp_modal_step4_paste_opened.png", full_page=True)

        # Inspect textarea in paste modal
        textareas = page.locator("textarea, [contenteditable='true']")
        print(f"Textareas count: {await textareas.count()}")
        if await textareas.count() > 0:
            await textareas.first.fill("테스트 본문 입력 성공!")
            await asyncio.sleep(1)

        insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert')").first
        print(f"Insert btn count: {await insert_btn.count()}")
        if await insert_btn.count() > 0:
            await insert_btn.click(force=True)
            await asyncio.sleep(6)

        await page.screenshot(path="temp_modal_step5_inserted.png", full_page=True)

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
