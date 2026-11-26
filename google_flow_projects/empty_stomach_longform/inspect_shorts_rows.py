# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def inspect_shorts_rows():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        
        page = None
        for pg in context.pages:
            if "studio.youtube.com" in pg.url:
                page = pg
                break
                
        if not page:
            return
            
        rows = page.locator("ytcp-video-row")
        count = await rows.count()
        print(f"Total rows: {count}")
        for i in range(count):
            row = rows.nth(i)
            title = await row.locator("#video-title").inner_text()
            date = await row.locator(".cell-body.tablecell-date").inner_text() if await row.locator(".cell-body.tablecell-date").count() > 0 else ""
            vid_anchor = await row.locator("#video-title").get_attribute("href") or ""
            print(f"[{i}] {title.strip()} | Date: {date.strip()} | Link: {vid_anchor}")

if __name__ == "__main__":
    asyncio.run(inspect_shorts_rows())

