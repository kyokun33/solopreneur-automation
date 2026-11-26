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

        # Click '복사된 텍스트'
        elem = page.get_by_text("복사된 텍스트", exact=True)
        if await elem.count() > 0:
            box = await elem.first.bounding_box()
            if box:
                await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                await asyncio.sleep(2)

        # Target the modal textarea (last textarea)
        textarea = page.locator("textarea").last
        print("Textarea found, filling...")
        await textarea.click(force=True)
        await textarea.fill("# [테스트 소스]\n\nConnect AI 1인기업 무인 자동화 프로젝트 소스 테스트입니다.")
        await asyncio.sleep(1)

        await page.screenshot(path="temp_modal_step6_text_filled.png", full_page=True)

        # Click insert button
        insert_btn = page.locator("button:has-text('삽입')").last
        if await insert_btn.count() > 0:
            print("Clicking insert button...")
            await insert_btn.click(force=True)
            await asyncio.sleep(7)

        await page.screenshot(path="temp_modal_step7_source_added.png", full_page=True)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
