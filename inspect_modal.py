import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    profile = r"C:\Users\sude3\.chrome_dev_profile"
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            profile,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        # Go directly to notebook page or create new one
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            await new_btn.click()
            await asyncio.sleep(4)

        print("Current URL:", page.url)

        # Inspect all buttons and text elements on the modal
        elements = await page.locator("button, textarea, input, div[role='button']").all_inner_texts()
        print("Elements found in modal:", elements[:30])

        # Check for title element
        title_elem = page.locator("text=/제목 없는|Untitled/i")
        print("Title elem count:", await title_elem.count())

        await page.screenshot(path="temp_modal_details.png", full_page=True)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
