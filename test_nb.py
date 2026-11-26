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
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        print("Page URL:", page.url)
        print("Page Title:", await page.title())

        # Find buttons
        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            text = await new_btn.inner_text()
            print(f"Clicking button: {text}")
            await new_btn.click()
            await asyncio.sleep(4)
            print("After click URL:", page.url)
            await page.screenshot(path="temp_nb_inside.png", full_page=True)
        else:
            print("New notebook button not found!")

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
