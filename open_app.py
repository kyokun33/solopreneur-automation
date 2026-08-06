import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Opening Chromium browser window on screen...")
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        print("Navigating to http://localhost:8000/ ...")
        await page.goto("http://localhost:8000/", wait_until="domcontentloaded")
        print("Browser window launched successfully!")
        
        # Keep browser open for user interaction
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
