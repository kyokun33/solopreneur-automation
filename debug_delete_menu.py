import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # Find 3 dots button on any card
        menu_btns = page.locator("button:has-text('more_vert'), button[aria-label*='옵션'], button[aria-label*='메뉴'], button[aria-label*='More']")
        print("Menu buttons count:", await menu_btns.count())

        if await menu_btns.count() > 0:
            # Click the second or third menu button (which belongs to an untitled notebook)
            target_btn = menu_btns.nth(2)
            print("Clicking menu button #2...")
            await target_btn.click(force=True)
            await asyncio.sleep(2)

            await page.screenshot(path="temp_menu_opened.png", full_page=True)

            # Inspect popup menu items
            menu_items = await page.locator("div[role='menu'] *, mat-menu-item, [role='menuitem']").all_inner_texts()
            print("Menu items found:", menu_items)

            # Look for delete text
            del_item = page.locator("[role='menuitem'], button, div").filter(has_text="삭제").first
            print("Delete item count:", await del_item.count())

            if await del_item.count() > 0:
                print("Clicking delete item...")
                await del_item.click(force=True)
                await asyncio.sleep(2)
                await page.screenshot(path="temp_delete_confirm_dialog.png", full_page=True)

                # Inspect buttons in dialog
                dialog_btns = await page.locator("mat-dialog-container button, div[role='dialog'] button, button").all_inner_texts()
                print("Dialog buttons:", dialog_btns[:10])

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
