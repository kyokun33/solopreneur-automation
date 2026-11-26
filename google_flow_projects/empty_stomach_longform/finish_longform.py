# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def fix_title_and_save():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        page = b.contexts[0].pages[0]
        
        title = "아침 공복에 '이것' 먹으면 위장이 녹아내립니다! 절대 피할 최악의 음식 3가지"
        desc = """아침에 건강 챙긴다고 공복에 무심코 먹었던 음식이 오히려 위장을 망가뜨리고 있었다면 어떨까요?
식사 대용으로 많이 찾는 바나나, 고구마, 모닝커피의 충격적인 진실과 의사들이 매일 아침 빈속에 챙겨 먹는 진짜 공복 보약 3가지를 공개합니다!

00:00 오프닝 & 공복 주의보
00:33 1. 바나나의 충격적인 진실 (심혈관 급증)
01:08 2. 고구마의 위벽 자극 (아교질 & 타닌)
01:42 3. 모닝커피의 위험성 (위산 역류)
02:14 4. 의사 추천 공복 보약 3가지 (미온수, 양배추, 달걀)
02:50 건강한 아침 습관 안내

#내몸에힐링 #건강정보 #공복음식 #건강상식 #아침식단 #1분건강"""

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
        }''', {'t': title, 'd': desc})
        
        await page.wait_for_timeout(1000)
        
        # Click next until step is VISIBILITY
        for i in range(4):
            cur_step = await page.evaluate('''() => {
                const d = document.querySelector('ytcp-uploads-dialog');
                return d ? d.getAttribute('workflow-step') : 'NO_DIALOG';
            }''')
            print(f"Step {i}: {cur_step}")
            if cur_step == 'VISIBILITY':
                break
            await page.evaluate('''() => {
                const btn = document.querySelector('ytcp-uploads-dialog #next-button');
                if (btn) btn.click();
            }''')
            await page.wait_for_timeout(1500)
            
        # In VISIBILITY, select PRIVATE
        await page.evaluate('''() => {
            const priv = document.querySelector('ytcp-uploads-dialog tp-yt-paper-radio-button[name="PRIVATE"]');
            if (priv) priv.click();
        }''')
        await page.wait_for_timeout(1500)
        
        # Click Done/Save
        await page.evaluate('''() => {
            const done = document.querySelector('ytcp-uploads-dialog #done-button');
            if (done) done.click();
        }''')
        print("Longform saved successfully!")
        await page.wait_for_timeout(5000)
        
        # Close dialog
        await page.evaluate('''() => {
            const closeBtn = document.querySelector('ytcp-uploads-dialog #close-button');
            if (closeBtn) closeBtn.click();
        }''')
        await page.wait_for_timeout(2000)
        print("Dialog closed.")

if __name__ == "__main__":
    asyncio.run(fix_title_and_save())

