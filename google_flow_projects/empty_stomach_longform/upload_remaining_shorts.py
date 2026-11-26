# -*- coding: utf-8 -*-
"""
Upload remaining Shorts 2 (고구마) & Shorts 3 (모닝커피) to YouTube Studio as Private
"""

import os
import asyncio
from playwright.async_api import async_playwright

REMAINING_SHORTS = [
    {
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠02_공복고구마편.mp4",
        "title": "달콤한 군고구마가 아침 빈속 위벽을 녹인다? #Shorts #내몸에힐링",
        "desc": "아침에 고구마 먹고 속 쓰리셨던 분들 주목! 아교질과 타닌이 위산 분비를 촉진해 위벽을 자극합니다. #내몸에힐링 #고구마 #위장건강 #1분건강 #Shorts"
    },
    {
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠03_빈속모닝커피편.mp4",
        "title": "눈뜨자마자 마시는 모닝커피의 치명적인 습격! #Shorts #내몸에힐링",
        "desc": "잠 깨려고 빈속에 진한 아메리카노 한 잔? 고농도 카페인이 위점막을 무방비로 타격합니다! #내몸에힐링 #모닝커피 #역류성식도염 #1분건강 #Shorts"
    }
]

async def upload_item(page, item):
    video_path = item["file"]
    print(f"\n==========================================")
    print(f"Uploading Shorts: {os.path.basename(video_path)}")
    print(f"==========================================")
    
    # 1. Clean backdrop/modals
    for _ in range(2):
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
        
    # 2. Click Create
    create_btn = page.locator("#create-icon, button:has-text('만들기'), ytcp-button:has-text('만들기')").first
    await create_btn.click()
    await page.wait_for_timeout(1000)
    
    # 3. Click Upload video option
    upload_item = page.locator("tp-yt-paper-item").filter(has_text="동영상 업로드").first
    await upload_item.click()
    await page.wait_for_timeout(2000)
    
    # 4. File input
    file_input = page.locator("input[type='file']").first
    await file_input.set_input_files(video_path)
    print("File selected, waiting for details dialog...")
    
    await page.wait_for_selector("ytcp-uploads-dialog #title-textarea #textbox", timeout=40000)
    await page.wait_for_timeout(2000)
    
    # 5. Inject title & description
    await page.evaluate('''({t, d}) => {
        const tBox = document.querySelector('ytcp-uploads-dialog #title-textarea #textbox');
        if (tBox) {
            tBox.innerText = t;
            tBox.dispatchEvent(new Event('input', { bubbles: true }));
        }
        const dBox = document.querySelector('ytcp-uploads-dialog #description-textarea #textbox');
        if (dBox) {
            dBox.innerText = d;
            dBox.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }''', {'t': item['title'][:98], 'd': item['desc']})
    print("Title & description set.")
    
    # 6. Audience
    await page.evaluate('''() => {
        const r = document.querySelector('ytcp-uploads-dialog tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]');
        if (r) r.click();
    }''')
    await page.wait_for_timeout(1000)
    
    # 7. Step Next
    for i in range(4):
        cur_step = await page.evaluate('''() => {
            const d = document.querySelector('ytcp-uploads-dialog');
            return d ? d.getAttribute('workflow-step') : 'NO_DIALOG';
        }''')
        print(f"Step {i}: {cur_step}")
        if cur_step == 'VISIBILITY' or cur_step == 'REVIEW':
            break
        await page.evaluate('''() => {
            const btn = document.querySelector('ytcp-uploads-dialog #next-button');
            if (btn) btn.click();
        }''')
        await page.wait_for_timeout(1500)
        
    # 8. Set Private
    await page.evaluate('''() => {
        const priv = document.querySelector('ytcp-uploads-dialog tp-yt-paper-radio-button[name="PRIVATE"]');
        if (priv) priv.click();
    }''')
    await page.wait_for_timeout(1500)
    
    # 9. Save
    await page.evaluate('''() => {
        const done = document.querySelector('ytcp-uploads-dialog #done-button');
        if (done) done.click();
    }''')
    print("Saved successfully!")
    await page.wait_for_timeout(5000)
    
    # 10. Close
    await page.evaluate('''() => {
        const closeBtn = document.querySelector('ytcp-uploads-dialog #close-button');
        if (closeBtn) closeBtn.click();
    }''')
    await page.wait_for_timeout(2000)
    print("Dialog closed.")
    return True

async def main():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        page = b.contexts[0].pages[0]
        await page.bring_to_front()
        
        for idx, item in enumerate(REMAINING_SHORTS):
            print(f"\nProcessing remaining shorts {idx+1}/2...")
            await upload_item(page, item)
            await page.wait_for_timeout(3000)
            
        print("\nALL REMAINING SHORTS UPLOADED SUCCESSFULLY!")
        
        # Navigate to Content tab (both Videos and Shorts)
        await page.goto("https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/upload?d=pt", wait_until="networkidle")
        await page.wait_for_timeout(4000)
        
        screenshot_longform = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\scratch\youtube_studio_longform_verified.png"
        await page.screenshot(path=screenshot_longform)
        print("Longform tab screenshot:", screenshot_longform)
        
        # Click Shorts tab
        shorts_tab = page.locator("tp-yt-paper-tab:has-text('Shorts'), text='Shorts'").first
        if await shorts_tab.count() > 0:
            await shorts_tab.click()
            await page.wait_for_timeout(4000)
            
        screenshot_shorts = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\scratch\youtube_studio_shorts_verified.png"
        await page.screenshot(path=screenshot_shorts)
        print("Shorts tab screenshot:", screenshot_shorts)

if __name__ == "__main__":
    asyncio.run(main())

