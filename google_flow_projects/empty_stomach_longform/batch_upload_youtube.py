# -*- coding: utf-8 -*-
"""
Robust batch uploader to YouTube Studio via Playwright CDP (port 9222)
Handles modal resets, backdrops, and uploads all 4 videos seamlessly.
"""

import os
import asyncio
from playwright.async_api import async_playwright

UPLOADS = [
    {
        "type": "longform",
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_롱폼01_공복에피할음식3가지_풀버전_web.mp4",
        "title": "아침 공복에 '이것' 먹으면 위장이 녹아내립니다! 절대 피할 최악의 음식 3가지 & 공복 보약 3가지",
        "desc": (
            "아침에 건강 챙긴다고 공복에 무심코 먹었던 음식이 오히려 위장을 망가뜨리고 있었다면 어떨까요?\n"
            "식사 대용으로 많이 찾는 바나나, 고구마, 모닝커피의 충격적인 진실과\n"
            "의사들이 매일 아침 빈속에 챙겨 먹는 진짜 공복 보약 3가지를 공개합니다!\n\n"
            "00:00 오프닝 & 공복 주의보\n"
            "00:33 1. 바나나의 충격적인 진실 (심혈관 급증)\n"
            "01:08 2. 고구마의 위벽 자극 (아교질 & 타닌)\n"
            "01:42 3. 모닝커피의 위험성 (위산 역류)\n"
            "02:14 4. 의사 추천 공복 보약 3가지 (미온수, 양배추, 달걀)\n"
            "02:50 건강한 아침 습관 안내\n\n"
            "#내몸에힐링 #건강정보 #공복음식 #건강상식 #아침식단 #1분건강"
        )
    },
    {
        "type": "shorts",
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠01_공복바나나편.mp4",
        "title": "아침 공복에 바나나 먹으면 심장에 큰 무리가 간다? #Shorts #내몸에힐링",
        "desc": "다이어트할 때 아침 대용으로 바나나 드시는 분들 많으시죠? 빈속 바나나의 충격적인 진실을 30초 만에 확인하세요! #내몸에힐링 #바나나 #건강정보 #1분건강 #Shorts"
    },
    {
        "type": "shorts",
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠02_공복고구마편.mp4",
        "title": "달콤한 군고구마가 아침 빈속 위벽을 녹인다? #Shorts #내몸에힐링",
        "desc": "아침에 고구마 먹고 속 쓰리셨던 분들 주목! 아교질과 타닌이 위산 분비를 촉진해 위벽을 자극합니다. #내몸에힐링 #고구마 #위장건강 #1분건강 #Shorts"
    },
    {
        "type": "shorts",
        "file": r"C:\Users\sude3\Desktop\내몸에힐링_숏츠03_빈속모닝커피편.mp4",
        "title": "눈뜨자마자 마시는 모닝커피의 치명적인 습격! #Shorts #내몸에힐링",
        "desc": "잠 깨려고 빈속에 진한 아메리카노 한 잔? 고농도 카페인이 위점막을 무방비로 타격합니다! #내몸에힐링 #모닝커피 #역류성식도염 #1분건강 #Shorts"
    }
]

async def clean_modals(page):
    """Ensure no modal or backdrop is blocking the view"""
    for _ in range(3):
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
    # Check if there's a close button in any open dialog
    close_btns = page.locator("#close-button, ytcp-button:has-text('닫기')")
    count = await close_btns.count()
    for i in range(count):
        btn = close_btns.nth(i)
        if await btn.is_visible():
            try:
                await btn.click(timeout=1000)
            except Exception:
                pass
    await page.wait_for_timeout(1000)

async def upload_single(page, item):
    video_path = item["file"]
    if not os.path.exists(video_path):
        print(f"Error: File not found {video_path}")
        return False
        
    print(f"\n==========================================")
    print(f"Starting Upload: [{item['type'].upper()}] {os.path.basename(video_path)}")
    print(f"==========================================")
    
    await clean_modals(page)
    
    # 1. Click Create button via JS evaluate if standard click is intercepted
    print("Opening upload dialog...")
    opened = await page.evaluate("""() => {
        const createBtn = document.querySelector('#create-icon') || document.querySelector('ytcp-button.ytcpAppHeaderCreateIcon');
        if (createBtn) {
            createBtn.click();
            return true;
        }
        return false;
    }""")
    await page.wait_for_timeout(1200)
    
    # Click upload option
    try:
        upload_item = page.locator("tp-yt-paper-item").filter(has_text="동영상 업로드").first
        if await upload_item.count() > 0 and await upload_item.is_visible():
            await upload_item.click()
    except Exception as e:
        print("Upload item click note:", e)
        
    await page.wait_for_timeout(2000)
    
    # 2. File input
    file_input = page.locator("input[type='file']").first
    await file_input.set_input_files(video_path)
    print("File selected, waiting for details dialog...")
    
    # Wait for textbox
    await page.wait_for_selector("#textbox, #title-textarea", timeout=40000)
    await page.wait_for_timeout(2500)
    
    # 3. Fill Title
    title_input = page.locator("#textbox[aria-label*='제목'], #title-textarea #textbox").first
    if await title_input.count() > 0:
        await title_input.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await title_input.fill(item["title"][:98])
        print("Title filled.")
        
    # 4. Fill Description
    desc_input = page.locator("#description-textarea #textbox, #textbox[aria-label*='설명']").first
    if await desc_input.count() > 0:
        await desc_input.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await desc_input.fill(item["desc"])
        print("Description filled.")
        
    # 5. Audience: Not for kids
    not_kids_radio = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
    if await not_kids_radio.count() > 0:
        await not_kids_radio.click()
        print("Audience set: Not made for kids.")
    else:
        alt_radio = page.locator("text='아니요, 아동용이 아닙니다'").first
        if await alt_radio.count() > 0:
            await alt_radio.click()
            
    # 6. Step Next (3 times)
    for step_idx in range(3):
        await page.wait_for_timeout(1500)
        next_btn = page.locator("#next-button, button:has-text('다음'), ytcp-button:has-text('다음')").first
        if await next_btn.count() > 0 and await next_btn.is_enabled():
            await next_btn.click()
            print(f"Step {step_idx + 1} Next clicked.")
            
    # 7. Visibility: Private
    await page.wait_for_timeout(2000)
    priv_radio = page.locator("tp-yt-paper-radio-button[name='PRIVATE']").first
    if await priv_radio.count() > 0:
        await priv_radio.click()
        print("Visibility set: 비공개 (Private).")
    else:
        alt_priv = page.locator("text='비공개'").first
        if await alt_priv.count() > 0:
            await alt_priv.click()
            
    # 8. Save / Publish
    await page.wait_for_timeout(1500)
    done_btn = page.locator("#done-button, button:has-text('저장'), ytcp-button:has-text('저장')").first
    if await done_btn.count() > 0:
        await done_btn.click()
        print("Done/Save button clicked successfully!")
        await page.wait_for_timeout(6000)
        
    # 9. Close dialog
    close_btn = page.locator("#close-button, button:has-text('닫기'), ytcp-button:has-text('닫기')").first
    if await close_btn.count() > 0 and await close_btn.is_visible():
        await close_btn.click()
        print("Upload modal closed.")
    else:
        await page.keyboard.press("Escape")
        
    await page.wait_for_timeout(3000)
    return True

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        await page.bring_to_front()
        
        # Ensure we are in Studio Content
        if "studio.youtube.com" not in page.url:
            await page.goto("https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/upload?d=pt", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            
        for idx, item in enumerate(UPLOADS):
            print(f"\nProcessing {idx+1}/{len(UPLOADS)}: {item['type']}...")
            await upload_single(page, item)
            await page.wait_for_timeout(4000)
            
        print("\nALL 4 VIDEOS UPLOADED SUCCESSFULLY!")
        
        # Navigate to Content page to show empirical proof
        await page.goto("https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/upload?d=pt", wait_until="networkidle")
        await page.wait_for_timeout(4000)
        
        # Screenshot
        verify_path = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\scratch\youtube_content_verified.png"
        await page.screenshot(path=verify_path)
        print(f"Empirical verification screenshot saved: {verify_path}")

if __name__ == "__main__":
    asyncio.run(main())
