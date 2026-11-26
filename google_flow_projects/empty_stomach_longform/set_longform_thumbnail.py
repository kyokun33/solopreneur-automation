# -*- coding: utf-8 -*-
import os
import asyncio
from playwright.async_api import async_playwright

async def set_longform_thumbnail():
    thumb_path = r"C:\Users\sude3\Desktop\내몸에힐링_롱폼_최종썸네일.jpg"
    if not os.path.exists(thumb_path):
        print("Thumbnail file not found!")
        return

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        
        target_page = None
        for pg in context.pages:
            if "studio.youtube.com" in pg.url:
                target_page = pg
                break
                
        if not target_page:
            print("Studio page not found! Creating new page...")
            target_page = await context.new_page()
            await target_page.goto("https://studio.youtube.com/video/W9KiwDJYcjI/edit", wait_until="networkidle")
        else:
            await target_page.bring_to_front()
            if "/edit" not in target_page.url:
                await target_page.goto("https://studio.youtube.com/video/W9KiwDJYcjI/edit", wait_until="networkidle")
            
        print("Connected to Studio page:", target_page.url)
        await target_page.wait_for_timeout(3000)
        
        print("Current URL:", target_page.url)
        
        # Find thumbnail section
        # YouTube Studio video details page has file input for thumbnail
        # Often input[type='file'][accept*='image'] or #file-loader
        file_inputs = target_page.locator("input[type='file']")
        count = await file_inputs.count()
        print(f"File inputs found: {count}")
        
        uploaded = False
        for i in range(count):
            inp = file_inputs.nth(i)
            accept = await inp.get_attribute("accept") or ""
            print(f"Input {i}: accept='{accept}'")
            if "image" in accept:
                print(f"Found thumbnail input at index {i}! Setting {thumb_path}...")
                await inp.set_input_files(thumb_path)
                uploaded = True
                break
                
        if not uploaded:
            # Try clicking custom thumbnail button/container
            thumb_uploader = target_page.locator("#still-picker #picker-item, #thumbnail-picker, ytcp-thumbnails-compact-editor, ytcp-thumbnail-editor").first
            print("Looking for thumbnail picker container...")
            if await thumb_uploader.count() > 0:
                print("Found thumbnail uploader container, looking for input within...")
                sub_input = thumb_uploader.locator("input[type='file']")
                if await sub_input.count() > 0:
                    await sub_input.set_input_files(thumb_path)
                    uploaded = True
                    
        await target_page.wait_for_timeout(3000)
        
        # Take screenshot of details page after thumbnail upload
        shot1 = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\thumbnail_uploaded_details.png"
        await target_page.screenshot(path=shot1)
        print("Screenshot saved:", shot1)
        
        # Click Save button (#save-button)
        save_btn = target_page.locator("#save-button, ytcp-button:has-text('저장'), ytcp-button:has-text('Save')").first
        if await save_btn.count() > 0:
            is_disabled = await save_btn.get_attribute("disabled")
            print("Save button disabled state:", is_disabled)
            if not is_disabled:
                print("Clicking Save button...")
                await save_btn.click()
                await target_page.wait_for_timeout(3000)
                print("Changes saved successfully!")
            else:
                print("Save button is disabled (maybe already saved or no change).")
                
        # Final screenshot
        shot2 = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\final_thumbnail_saved.png"
        await target_page.screenshot(path=shot2)
        print("Final screenshot saved:", shot2)

if __name__ == "__main__":
    asyncio.run(set_longform_thumbnail())

