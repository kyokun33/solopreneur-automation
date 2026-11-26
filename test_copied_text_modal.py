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

        # Click '복사된 텍스트'
        print("Clicking '복사된 텍스트' button...")
        btn = page.locator("button, div, span").filter(has_text="복사된 텍스트").first
        if await btn.count() > 0:
            print("Found '복사된 텍스트' button, clicking!")
            await btn.click(force=True)
            await asyncio.sleep(3)
        else:
            print("'복사된 텍스트' button not found!")

        await page.screenshot(path="temp_modal_step3_copied_text.png", full_page=True)

        # Log inputs in the new modal view
        inputs = await page.locator("textarea, input, [contenteditable='true']").all()
        print(f"Inputs count: {len(inputs)}")
        for idx, el in enumerate(inputs):
            ph = await el.get_attribute("placeholder") or ""
            print(f"Input #{idx}: placeholder={ph}")

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
