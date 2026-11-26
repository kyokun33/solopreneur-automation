# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def check_shorts():
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
        # Go to shorts tab
        await target_page.goto("https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/short?filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D", wait_until="networkidle")
        await target_page.wait_for_timeout(3000)
        
        rows = target_page.locator("ytcp-video-row")
        count = await rows.count()
        print(f"Total Shorts rows: {count}")
        for i in range(count):
            title_el = rows.nth(i).locator("#video-title")
            t_text = await title_el.inner_text() if await title_el.count() > 0 else "No title"
            print(f"Shorts [{i}]: {t_text.strip()}")
            
        shot = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a\studio_shorts_tab_view.png"
        await target_page.screenshot(path=shot)
        print("Shorts tab screenshot saved:", shot)

if __name__ == "__main__":
    asyncio.run(check_shorts())

