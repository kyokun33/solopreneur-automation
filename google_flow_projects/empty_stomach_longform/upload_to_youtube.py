# -*- coding: utf-8 -*-
"""
Upload video to YouTube Studio via Playwright CDP (port 9222)
Usage: python upload_to_youtube.py <video_path> <title> <description> <tags>
"""

import sys
import os
import asyncio
from playwright.async_api import async_playwright

async def upload_video(video_path, title, description, tags):
    if not os.path.exists(video_path):
        print(f"Error: File not found {video_path}")
        return False

    print(f"Connecting to Chrome CDP on port 9222...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find YouTube Studio page
            target_page = None
            for pg in context.pages:
                if "studio.youtube.com" in pg.url:
                    target_page = pg
                    break
            
            if not target_page:
                target_page = await context.new_page()
                await target_page.goto("https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/upload?d=pt", wait_until="networkidle")
            else:
                await target_page.bring_to_front()
                
            print(f"Connected to page: {target_page.url}")
            
            # Navigate to videos/upload if not already in modal
            upload_input = target_page.locator("input[type='file']")
            input_count = await upload_input.count()
            
            if input_count == 0:
                print("Opening Create / Upload modal...")
                create_btn = target_page.locator("#create-icon, button:has-text('만들기'), ytcp-button:has-text('만들기')").first
                if await create_btn.count() > 0:
                    await create_btn.click()
                    await target_page.wait_for_timeout(1000)
                    upload_option = target_page.locator("text='동영상 업로드'").first
                    await upload_option.click()
                    await target_page.wait_for_timeout(2000)
            
            # Set input file
            print(f"Setting input file: {video_path}")
            upload_input = target_page.locator("input[type='file']").first
            await upload_input.set_input_files(video_path)
            
            # Wait for upload modal to initialize
            print("Waiting for details dialog...")
            await target_page.wait_for_selector("#textbox, #title-textarea", timeout=30000)
            await target_page.wait_for_timeout(2000)
            
            # 1. Fill Title
            print(f"Setting Title: {title}")
            title_input = target_page.locator("#textbox[aria-label*='제목'], #title-textarea #textbox").first
            if await title_input.count() > 0:
                await title_input.click()
                await target_page.keyboard.press("Control+A")
                await target_page.keyboard.press("Backspace")
                await title_input.fill(title[:100])
                
            # 2. Fill Description
            print(f"Setting Description...")
            desc_input = target_page.locator("#description-textarea #textbox, #textbox[aria-label*='설명']").first
            if await desc_input.count() > 0:
                await desc_input.click()
                await target_page.keyboard.press("Control+A")
                await target_page.keyboard.press("Backspace")
                await desc_input.fill(description)
                
            # 3. Audience: Not made for kids
            print("Selecting '아동용이 아닙니다'...")
            not_kids_radio = target_page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
            if await not_kids_radio.count() > 0:
                await not_kids_radio.click()
            else:
                radio_by_text = target_page.locator("text='아니요, 아동용이 아닙니다'").first
                if await radio_by_text.count() > 0:
                    await radio_by_text.click()
                    
            # Click Next through steps to Visibility
            print("Navigating through wizard steps...")
            for step in range(3):
                next_btn = target_page.locator("#next-button, button:has-text('다음'), ytcp-button:has-text('다음')").first
                if await next_btn.count() > 0 and await next_btn.is_enabled():
                    await next_btn.click()
                    await target_page.wait_for_timeout(1500)
                    
            # 4. Visibility: Private (비공개)
            print("Setting Visibility to 비공개 (Private)...")
            private_radio = target_page.locator("tp-yt-paper-radio-button[name='PRIVATE']").first
            if await private_radio.count() > 0:
                await private_radio.click()
            else:
                priv_text = target_page.locator("text='비공개'").first
                if await priv_text.count() > 0:
                    await priv_text.click()
                    
            await target_page.wait_for_timeout(1000)
            
            # 5. Save / Publish
            print("Clicking Save / 완료...")
            save_btn = target_page.locator("#done-button, button:has-text('저장'), ytcp-button:has-text('저장')").first
            if await save_btn.count() > 0:
                await save_btn.click()
                print("Save button clicked successfully!")
                await target_page.wait_for_timeout(4000)
                
            # Close dialog if '닫기' exists
            close_btn = target_page.locator("#close-button, button:has-text('닫기'), ytcp-button:has-text('닫기')").first
            if await close_btn.count() > 0 and await close_btn.is_visible():
                await close_btn.click()
                await target_page.wait_for_timeout(1000)
                
            print("Upload sequence completed successfully!")
            return True
            
        except Exception as e:
            print(f"Exception during upload: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_to_youtube.py <video_path> <title> [desc]")
        sys.exit(1)
        
    v_path = sys.argv[1]
    v_title = sys.argv[2]
    v_desc = sys.argv[3] if len(sys.argv) > 3 else ""
    
    asyncio.run(upload_video(v_path, v_title, v_desc, ""))

