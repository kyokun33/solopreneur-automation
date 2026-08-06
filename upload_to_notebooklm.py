import asyncio
import os
from playwright.async_api import async_playwright

DOCUMENT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_1인기업_수익화아이템3.md"

async def main():
    if not os.path.exists(DOCUMENT_PATH):
        print(f"File not found: {DOCUMENT_PATH}")
        return

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("Launching Chromium browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("Navigating to https://notebooklm.google.com/ ...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # Look for Create / New Notebook button
        create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create']")
        if await create_btn.count() > 0:
            print("Found Create button. Clicking...")
            await create_btn.first.click()
            await asyncio.sleep(4)

        # Check for file input element for direct upload
        file_input = page.locator("input[type='file']")
        if await file_input.count() > 0:
            print(f"Found file input! Uploading {DOCUMENT_PATH} ...")
            await file_input.first.set_input_files(DOCUMENT_PATH)
            print("File set! Waiting for upload to complete...")
            await asyncio.sleep(10)
        else:
            # Fallback: look for Copied text or textarea
            print("Checking text input options...")
            text_option = page.locator("text=/Copied text|복사한 텍스트|붙여넣기|Text/")
            if await text_option.count() > 0:
                await text_option.first.click()
                await asyncio.sleep(2)

            textarea = page.locator("textarea, [contenteditable='true']")
            if await textarea.count() > 0:
                print("Pasting content into text area...")
                await textarea.first.fill(content)
                await asyncio.sleep(2)
                
                insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입'), button:has-text('저장'), button:has-text('확인')")
                if await insert_btn.count() > 0:
                    await insert_btn.first.click()
                    print("Inserted content successfully!")
                    await asyncio.sleep(8)

        print("Finished process.")
        await asyncio.sleep(5)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
