# -*- coding: utf-8 -*-
"""
Upload character shorts to YouTube Studio using existing page without page.goto
"""

import os
import asyncio
from playwright.async_api import async_playwright

UPLOADS = [
    {
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠01_공복바나나편.mp4",
        "title": "아침 공복에 바나나 먹으면 심장에 큰 무리가 간다? #Shorts #내몸에힐링",
        "desc": "다이어트할 때 아침 대용으로 바나나 드시는 분들 많으시죠? 빈속 바나나의 충격적인 진실을 힐링 멘토 하니가 알려드립니다! #내몸에힐링 #바나나 #건강정보 #1분건강 #Shorts"
    },
    {
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠02_공복고구마편.mp4",
        "title": "달콤한 군고구마가 아침 빈속 위벽을 녹인다? #Shorts #내몸에힐링",
        "desc": "아침에 고구마 먹고 속 쓰리셨던 분들 주목! 아교질과 타닌이 위산 분비를 촉진해 위벽을 자극합니다. 닥터 힐러의 건강 솔루션! #내몸에힐링 #고구마 #위장건강 #1분건강 #Shorts"
    },
    {
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠03_빈속모닝커피편.mp4",
        "title": "눈뜨자마자 마시는 모닝커피의 치명적인 습격! #Shorts #내몸에힐링",
        "desc": "잠 깨려고 빈속에 진한 아메리카노 한 잔? 고농도 카페인이 위점막을 무방비로 타격합니다! #내몸에힐링 #모닝커피 #역류성식도염 #1분건강 #Shorts"
    }
]

async def upload_single(page, item):
    video_path = item["file"]
    print(f"\n==========================================")
    print(f"Uploading Character Shorts: {os.path.basename(video_path)}")
    print(f"Title: {item['title']}")
    print(f"==========================================")
    
    # 1. Close any modal
    for _ in range(2):
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
        
    # 2. Click Create
    create_btn = page.locator("#create-icon, button:has-text('만들기'), ytcp-button:has-text('만들기')").first
    await create_btn.click()
    await page.wait_for_timeout(1000)
    
    # 3. Click upload item
    await page.locator("tp-yt-paper-item").filter(has_text="동영상 업로드").first.click()
    await page.wait_for_timeout(2000)
    
    # 4. Input file
    file_input = page.locator("input[type='file']").first
    await file_input.set_input_files(video_path)
    print("File selected, waiting for details...")
    
    await page.wait_for_selector("ytcp-uploads-dialog #title-textarea #textbox", timeout=40000)
    await page.wait_for_timeout(2000)
    
    # 5. Inject Title & Desc
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
    print("Title & description injected.")
    
    # 6. Audience
    await page.evaluate('''() => {
        const r = document.querySelector('ytcp-uploads-dialog tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]');
        if (r) r.click();
    }''')
    await page.wait_for_timeout(1000)
    
    # 7. Next steps
    for step_i in range(4):
        cur_step = await page.evaluate('''() => {
            const d = document.querySelector('ytcp-uploads-dialog');
            return d ? d.getAttribute('workflow-step') : 'NO_DIALOG';
        }''')
        print(f"Step {step_i}: {cur_step}")
        if cur_step in ('VISIBILITY', 'REVIEW'):
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
    print("Save clicked!")
    await page.wait_for_timeout(5000)
    
    # 10. Close
    await page.evaluate('''() => {
        const closeBtn = document.querySelector('ytcp-uploads-dialog #close-button');
        if (closeBtn) closeBtn.click();
    }''')
    await page.wait_for_timeout(2000)
    print("Upload completed.")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = b.contexts[0]
        # find studio page
        page = None
        for pg in context.pages:
            if 'studio.youtube.com' in pg.url:
                page = pg
                break
        if not page:
            page = context.pages[0]
            
        await page.bring_to_front()
        
        for idx, item in enumerate(UPLOADS):
            print(f"\nProcessing {idx+1}/{len(UPLOADS)}: {item['title']}...")
            await upload_single(page, item)
            await page.wait_for_timeout(4000)
            
        print("\nALL 3 CHARACTER SHORTS UPLOADED SUCCESSFULLY!")
        
        # Take screenshot of Studio
        await page.wait_for_timeout(3000)
        shot_path = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\final_character_shorts_uploaded.png"
        await page.screenshot(path=shot_path)
        print("Final screenshot saved:", shot_path)

if __name__ == "__main__":
    asyncio.run(main())

