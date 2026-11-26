# -*- coding: utf-8 -*-
"""
Delete all Shorts from YouTube Studio Content tab cleanly
"""

import asyncio
from playwright.async_api import async_playwright

async def delete_shorts():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = b.contexts[0]
        page = None
        for pg in context.pages:
            if "studio.youtube.com" in pg.url:
                page = pg
                break
        if not page:
            page = await context.new_page()
            
        await page.goto("https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/short?d=ud", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # Check rows
        rows = page.locator("ytcp-video-row")
        count = await rows.count()
        print(f"Total shorts rows found: {count}")
        if count == 0:
            print("No shorts to delete.")
            return
            
        # Select all checkbox on header
        header_cb = page.locator("ytcp-checkbox-lit#select-all-checkbox, #select-all-checkbox tp-yt-paper-checkbox").first
        if await header_cb.count() == 0:
            header_cb = page.locator("#select-all-checkbox").first
            
        print("Clicking select all checkbox...")
        await header_cb.click()
        await page.wait_for_timeout(2000)
        
        # Check if selection bar appears
        # Look for "추가 작업" or "더보기"
        more_btn = page.locator("ytcp-bulk-actions #actions-menu-button, ytcp-button:has-text('추가 작업'), ytcp-button:has-text('더보기')").first
        if await more_btn.count() > 0:
            await more_btn.click()
            await page.wait_for_timeout(1000)
            
            # Click "완전 삭제"
            del_item = page.locator("tp-yt-paper-item:has-text('완전 삭제'), text='완전 삭제'").first
            if await del_item.count() > 0:
                await del_item.click()
                await page.wait_for_timeout(1500)
                
                # In confirmation dialog, check checkbox "동영상이 완전히 삭제되며 되돌릴 수 없음을 이해합니다"
                confirm_cb = page.locator("ytcp-confirmation-dialog tp-yt-paper-checkbox, ytcp-confirmation-dialog ytcp-checkbox-lit").first
                if await confirm_cb.count() > 0:
                    await confirm_cb.click()
                    await page.wait_for_timeout(1000)
                    
                # Click Confirm button
                confirm_btn = page.locator("ytcp-confirmation-dialog #confirm-button, ytcp-confirmation-dialog ytcp-button:has-text('완전 삭제')").first
                if await confirm_btn.count() > 0:
                    await confirm_btn.click()
                    print("Successfully deleted all shorts via bulk actions!")
                    await page.wait_for_timeout(6000)
                    return
                    
        # Fallback: Delete rows one by one
        print("Bulk delete not available or failed. Deleting one by one...")
        while True:
            first_row = page.locator("ytcp-video-row").first
            if await first_row.count() == 0:
                print("All rows deleted!")
                break
            await first_row.hover()
            await page.wait_for_timeout(500)
            
            # Hover options menu
            opt_btn = first_row.locator("#hover-items #options-button, #options-button").first
            if await opt_btn.count() > 0:
                await opt_btn.click()
                await page.wait_for_timeout(1000)
                del_opt = page.locator("tp-yt-paper-item:has-text('완전 삭제'), text='완전 삭제'").first
                if await del_opt.count() > 0:
                    await del_opt.click()
                    await page.wait_for_timeout(1500)
                    cb = page.locator("ytcp-confirmation-dialog tp-yt-paper-checkbox, ytcp-confirmation-dialog ytcp-checkbox-lit").first
                    if await cb.count() > 0:
                        await cb.click()
                        await page.wait_for_timeout(500)
                    c_btn = page.locator("ytcp-confirmation-dialog #confirm-button").first
                    if await c_btn.count() > 0:
                        await c_btn.click()
                        print("One short deleted.")
                        await page.wait_for_timeout(4000)
            else:
                break
                
        print("Shorts deletion process complete.")

if __name__ == "__main__":
    asyncio.run(delete_shorts())

