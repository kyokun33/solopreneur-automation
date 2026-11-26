# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def inspect_studio():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        
        target_page = None
        for pg in context.pages:
            if "studio.youtube.com" in pg.url:
                target_page = pg
                break
                
        if not target_page:
            print("Studio page not found!")
            return
            
        await target_page.bring_to_front()
        print("Page URL:", target_page.url)
        await target_page.wait_for_timeout(3000)
        
        # Take screenshot of current state
        shot_path = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\current_studio_view.png"
        await target_page.screenshot(path=shot_path)
        print("Screenshot saved:", shot_path)
        
        # Check rows
        rows = target_page.locator("ytcp-video-row")
        count = await rows.count()
        print(f"Total video rows: {count}")
        for i in range(min(5, count)):
            title_el = rows.nth(i).locator("#video-title")
            t_text = await title_el.inner_text() if await title_el.count() > 0 else "No title"
            print(f"[{i}] {t_text.strip()}")

if __name__ == "__main__":
    asyncio.run(inspect_studio())

