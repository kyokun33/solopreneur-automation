import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def main():
    html_path = os.path.abspath(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ebook_reader.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    
    async with async_playwright() as p:
        print(f"Launching browser window on monitor: {file_url}")
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--disable-infobars",
                "--app=" + file_url
            ]
        )
        context = await browser.new_context(no_viewport=True)
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(file_url, wait_until="domcontentloaded")
        print("Browser window successfully opened on monitor!")
        
        # Keep window active
        await asyncio.sleep(86400)

if __name__ == "__main__":
    asyncio.run(main())
